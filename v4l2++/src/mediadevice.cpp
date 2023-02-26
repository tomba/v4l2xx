#include <fmt/format.h>

#include <string>
#include <algorithm>

#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <sys/ioctl.h>
#include <unistd.h>
#include <system_error>
#include <sys/sysmacros.h>
#include <cassert>

#include <linux/media.h>
#include <linux/v4l2-subdev.h>

#include <v4l2++/mediadevice.h>
#include <v4l2++/videodevice.h>
#include <v4l2++/videosubdev.h>
#include <v4l2++/helpers.h>

using namespace std;
using namespace v4l2;

static string to_lower(const string& str)
{
	string data = str;
	transform(data.begin(), data.end(), data.begin(), ::tolower);
	return data;
}

static string filepath_for_major_minor(uint32_t major, uint32_t minor)
{
	int r;

	for (int i = 0; i < 20; ++i) {
		struct stat statbuf;

		string path = fmt::format("/dev/video{}", i);

		r = stat(path.c_str(), &statbuf);
		if (r)
			break;

		if (::major(statbuf.st_rdev) == major && ::minor(statbuf.st_rdev) == minor)
			return path;
	}

	for (int i = 0; i < 20; ++i) {
		struct stat statbuf {
		};

		string path = fmt::format("/dev/v4l-subdev{}", i);

		r = stat(path.c_str(), &statbuf);
		if (r)
			break;

		if (::major(statbuf.st_rdev) == major && ::minor(statbuf.st_rdev) == minor)
			return path;
	}

	throw runtime_error(fmt::format("dev node not found for major,minor {},{}", major, minor));
}

/* V4L2 helper funcs */

static void v4l2_get_device_info(int fd, MediaDevicePriv* priv)
{
	int r;

	priv->info = {};

	r = ioctl(fd, MEDIA_IOC_DEVICE_INFO, &priv->info);
	THROW_IF(r, "MEDIA_IOC_DEVICE_INFO failed: {}", r);
}

template<typename T>
shared_ptr<T> find_object(MediaDevicePriv* priv, uint32_t id)
{
	auto i = find_if(priv->objects.begin(), priv->objects.end(), [id](const auto& o) { return o->id() == id; });
	if (i == priv->objects.end())
		throw runtime_error("MediaObject not found");
	shared_ptr<MediaObject> o = *i;
	shared_ptr<T> ret = dynamic_pointer_cast<T>(o);
	return ret;
}

static void v4l2_get_topology(int fd, MediaDevicePriv* priv)
{
	struct media_v2_topology topology {
	};
	int r;

	r = ioctl(fd, MEDIA_IOC_G_TOPOLOGY, &topology);
	THROW_IF(r, "MEDIA_IOC_G_TOPOLOGY call 1 failed: {}", r);

	media_v2_entity entities[topology.num_entities];
	media_v2_interface interfaces[topology.num_interfaces];
	media_v2_pad pads[topology.num_pads];
	media_v2_link links[topology.num_links];

	memset(entities, 0, sizeof(entities));
	memset(interfaces, 0, sizeof(interfaces));
	memset(pads, 0, sizeof(pads));
	memset(links, 0, sizeof(links));

	topology.ptr_entities = (uint64_t)&entities;
	topology.ptr_interfaces = (uint64_t)&interfaces;
	topology.ptr_pads = (uint64_t)&pads;
	topology.ptr_links = (uint64_t)&links;

	r = ioctl(fd, MEDIA_IOC_G_TOPOLOGY, &topology);
	THROW_IF(r, "MEDIA_IOC_G_TOPOLOGY call 2 failed: {}", r);

	for (const auto& info : entities) {
		auto ob = make_shared<MediaEntity>(priv->media_device);
		ob->info = info;
		priv->objects.push_back(ob);
	}

	for (const auto& info : interfaces) {
		auto ob = make_shared<MediaInterface>(priv->media_device);
		ob->info = info;
		priv->objects.push_back(ob);
	}

	for (const auto& info : pads) {
		auto ob = make_shared<MediaPad>(priv->media_device);
		ob->info = info;
		priv->objects.push_back(ob);

		shared_ptr<MediaEntity> ent = find_object<MediaEntity>(priv, info.entity_id);
		ent->pads.resize(info.index + 1);
		ent->pads[info.index] = ob;

		ob->entity = ent;
	}

	for (const auto& info : links) {
		auto link = make_shared<MediaLink>(priv->media_device);
		link->info = info;
		priv->objects.push_back(link);

		shared_ptr<MediaObject> src = find_object<MediaObject>(priv, info.source_id);
		link->source = src;

		shared_ptr<MediaObject> dst = find_object<MediaObject>(priv, info.sink_id);
		link->sink = dst;

		if (auto pad = dynamic_pointer_cast<MediaPad>(src)) {
			pad->links.push_back(link);
		} else if (auto iface = dynamic_pointer_cast<MediaInterface>(src)) {
			THROW_IF(iface->link, "iface->link already set");
			iface->link = link;
		} else if (auto ent = dynamic_pointer_cast<MediaEntity>(src)) {
			THROW_IF(ent->link, "ent->link already set");
			ent->link = link;
		} else {
			THROW("Unhandled object when iterating links");
		}

		if (auto pad = dynamic_pointer_cast<MediaPad>(dst)) {
			pad->links.push_back(link);
		} else if (auto iface = dynamic_pointer_cast<MediaInterface>(dst)) {
			THROW_IF(iface->link, "iface->link already set");
			iface->link = link;
		} else if (auto ent = dynamic_pointer_cast<MediaEntity>(dst)) {
			THROW_IF(ent->link, "ent->link already set");
			ent->link = link;
		} else {
			THROW("Unhandled object when iterating links");
		}
	}
}

static void v4l2_get_descs(int fd, MediaDevicePriv* priv)
{
	for (auto& ob : priv->objects) {
		auto ent = dynamic_pointer_cast<MediaEntity>(ob);
		if (!ent)
			continue;

		uint32_t eid = ent->id();

		int r;

		ent->desc = {};
		ent->desc.id = eid;

		r = ioctl(fd, MEDIA_IOC_ENUM_ENTITIES, &ent->desc);
		THROW_IF(r, "MEDIA_IOC_ENUM_ENTITIES failed: {}", r);

		struct media_pad_desc pad_descs[ent->desc.pads];
		struct media_link_desc link_descs[ent->desc.links];

		memset(pad_descs, 0, sizeof(pad_descs));
		memset(link_descs, 0, sizeof(link_descs));

		struct media_links_enum links_enum {
		};

		links_enum.entity = eid;
		links_enum.pads = pad_descs;
		links_enum.links = link_descs;

		r = ioctl(fd, MEDIA_IOC_ENUM_LINKS, &links_enum);
		THROW_IF(r, "MEDIA_IOC_ENUM_LINKS failed: {}", r);

		for (const auto& desc : pad_descs) {
			auto ent = find_object<MediaEntity>(priv, desc.entity);
			ent->pads[desc.index]->desc = desc;
		}

		for (const auto& desc : link_descs) {
			auto ent = find_object<MediaEntity>(priv, desc.source.entity);
			auto pad = ent->pads[desc.source.index];
			//pad->link->desc = desc; // XXX we can't find the correct link
		}
	}
}
#if 0
static void v4l2_set_link(int fd)
{
	struct media_link_desc desc;
	int r;

	r = ioctl(fd, MEDIA_IOC_SETUP_LINK, &desc);
	THROW_IF(r, "MEDIA_IOC_ENUM_ENTITIES failed: {}", r);

}
#endif

MediaDevice::MediaDevice(const string& dev)
	: MediaDevice(::open(dev.c_str(), O_RDWR))
{
}

MediaDevice::MediaDevice(int fd)
	: m_fd(fd)
{
	if (fd < 0)
		throw runtime_error("bad fd");

	m_priv = new MediaDevicePriv;
	m_priv->media_device = this;

	v4l2_get_device_info(fd, m_priv);
	v4l2_get_topology(fd, m_priv);
	v4l2_get_descs(fd, m_priv);

	// Setup devices

	for (auto& ob : m_priv->objects) {
		auto ent = dynamic_pointer_cast<MediaEntity>(ob);
		if (!ent)
			continue;

		if (!ent->link) {
			fmt::print("no link\n");
			continue;
		}

		auto iface = dynamic_pointer_cast<MediaInterface>(ent->link->source);
		if (!iface) {
			fmt::print("no iface\n");
			continue;
		}

		string path = filepath_for_major_minor(iface->info.devnode.major, iface->info.devnode.minor);
		ent->dev_path = path;

		if (ent->is_subdev())
			ent->subdev = make_unique<VideoSubdev>(path);
		else
			ent->dev = make_unique<VideoDevice>(path);
	}
}

MediaDevice::~MediaDevice()
{
	::close(m_fd);
	delete m_priv;
}
#define HACK_STREAM 0

static void print_entity(const MediaEntity* ent)
{
	const auto& e = ent->info;

	fmt::print("Entity {}: '{}', {:#x}, {:#x}, {}\n", e.id, e.name, e.function, e.flags, ent->dev_path);

	const auto& desc = ent->desc;

	fmt::print("  Desc: '{}', {:#x}, {:#x}, ({}/{})\n", desc.name, desc.type, desc.flags, desc.dev.major, desc.dev.minor);

	for (auto& pad : ent->pads) {
		const auto& i = pad->info;
		const auto& d = pad->desc;

		fmt::print("  Pad {}: {}/{}, {:#x}\n", i.id, i.entity_id, i.index, i.flags);
		fmt::print("    Desc: {}: flags {:#x}, ent {}\n", d.index, d.flags, d.entity);

		for (auto& link : pad->links) {
			fmt::print("    Pad Link: id {}, {} -> {}\n", link->id(), link->source->id(), link->sink->id());
		}

		if (pad->entity && pad->entity->is_subdev()) {
			uint32_t width;
			uint32_t height;
			BusFormat fmt;

			int ret = pad->entity->subdev->get_format(i.index, HACK_STREAM, width, height, fmt);
			if (!ret)
				fmt::print("    {}x{}, {}\n", width, height, BusFormatToString(fmt));
		}
	}

	fmt::print("\n");
}

void MediaDevice::print(const string& name) const
{
	auto p = m_priv;

	if (name.empty()) {
		fmt::print("=== {}, {}, {}, {} ===\n\n", p->info.driver, p->info.model, p->info.serial, p->info.bus_info);

		for (auto& ob : p->objects) {
			if (auto ent = dynamic_pointer_cast<MediaEntity>(ob))
				print_entity(ent.get());
		}

		for (auto& ob : p->objects) {
			if (auto iface = dynamic_pointer_cast<MediaInterface>(ob)) {
				const auto& i = iface->info;
				fmt::print("InterfaceV2 {}: {:#x}, {:#x}, ({}/{})\n", i.id, i.intf_type, i.flags, i.devnode.major, i.devnode.minor);
			}
		}

		for (auto& ob : p->objects) {
			if (auto link = dynamic_pointer_cast<MediaLink>(ob)) {
				const auto& i = link->info;
				const auto& d = link->desc;
				fmt::print("LinkV2 {}: {} -> {}, {:#x}\n", i.id, i.source_id, i.sink_id, i.flags);
				fmt::print("  Desc: link {}/{} -> {}/{}, {:#x}\n", d.source.entity, d.source.index, d.sink.entity, d.sink.index, d.flags);
			}
		}
	} else {
		vector<MediaEntity*> entities = collect_entities(name);

		for (auto e : entities) {
			if (!e->is_subdev())
				continue;

			print_entity(e);
		}
	}
}

MediaEntity* MediaDevice::find_entity(const string& name) const
{
	for (auto& ob : m_priv->objects) {
		if (auto ent = dynamic_pointer_cast<MediaEntity>(ob)) {
			const auto& e = ent->info;
			if (to_lower(name) == to_lower(e.name))
				return ent.get();
		}
	}

	for (auto& ob : m_priv->objects) {
		if (auto ent = dynamic_pointer_cast<MediaEntity>(ob)) {
			const auto& e = ent->info;
			if (to_lower(e.name).find(to_lower(name)) != string::npos)
				return ent.get();
		}
	}

	return nullptr;
}

vector<MediaEntity*> MediaDevice::collect_entities(const string& name) const
{
	if (name.empty()) {
		vector<MediaEntity*> l;

		for (auto& ob : m_priv->objects) {
			if (auto ent = dynamic_pointer_cast<MediaEntity>(ob))
				l.push_back(ent.get());
		}

		return l;
	}

	MediaEntity* first_ent = find_entity(name);

	if (!first_ent)
		throw runtime_error("entity not found\n");

	vector<MediaEntity*> work_list{ first_ent };
	vector<MediaEntity*> entities{ first_ent };
#if 0
	while (!work_list.empty()) {
		MediaEntity* ent = work_list.back();
		work_list.pop_back();

		//for (const auto& pd : ent->pad_descs) {
		//	m_priv->pad_descs[0][0]
		//
		//}

		for (auto& ld : ent->link_descs) {
			assert(ld.source.entity == ent->entity_data.id);

			MediaEntity* dst = &m_priv->ents.at(ld.sink.entity);

			if (find(entities.begin(), entities.end(), dst) != entities.end())
				continue;

			work_list.push_back(dst);
			entities.push_back(dst);
			fmt::print("add dst {}\n", dst->entity_data.name);

			MediaEntity* src = &m_priv->ents.at(ld.source.entity);

			if (find(entities.begin(), entities.end(), src) != entities.end())
				continue;

			work_list.push_back(src);
			entities.push_back(src);
			fmt::print("add src {}\n", src->entity_data.name);
		}
	}
#endif
	return entities;
}

bool MediaEntity::is_subdev() const
{
	if (!link)
		return false;

	auto iface = dynamic_pointer_cast<MediaInterface>(link->source);
	if (!iface)
		return false;

	return iface->info.intf_type == MEDIA_INTF_T_V4L_SUBDEV;
}

vector<MediaEntity*> MediaEntity::get_linked_entities(uint32_t pad_idx)
{
	THROW_IF(pad_idx >= this->pads.size(), "Bad pad index");

	vector<MediaEntity*> v;

	auto& pad = this->pads[pad_idx];

	for (auto& link : pad->links) {
		shared_ptr<MediaObject> remote_ob;
		if (pad->info.flags & MEDIA_PAD_FL_SINK)
			remote_ob = link->source;
		else if (pad->info.flags & MEDIA_PAD_FL_SOURCE)
			remote_ob = link->sink;
		else
			THROW("Bad pad flags");

		shared_ptr<MediaPad> remote_pad = dynamic_pointer_cast<MediaPad>(remote_ob);
		THROW_IF(!remote_pad, "Failed to get remote pad");
		THROW_IF(!remote_pad->entity, "No entity for remote pad");

		v.push_back(remote_pad->entity.get());
	}

	return v;
}

vector<MediaLink*> MediaEntity::get_links(uint32_t pad_idx)
{
	THROW_IF(pad_idx >= this->pads.size(), "Bad pad index");

	vector<MediaLink*> v;

	auto& pad = this->pads[pad_idx];

	for (auto& link : pad->links)
		v.push_back(link.get());

	return v;
}

void MediaEntity::setup_link(MediaLink* ml)
{
	int r;

	struct media_link_desc desc {};

	shared_ptr<MediaPad> source = dynamic_pointer_cast<MediaPad>(ml->source);
	shared_ptr<MediaPad> sink = dynamic_pointer_cast<MediaPad>(ml->sink);

	desc.source = source->desc;
	desc.sink = sink->desc;
	desc.flags = ml->info.flags;

	r = ioctl(m_media_device->fd(), MEDIA_IOC_SETUP_LINK, &desc);
	THROW_IF(r, "MEDIA_IOC_SETUP_LINK failed: {}", r);
}
