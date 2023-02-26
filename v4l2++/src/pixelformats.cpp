#include <map>

#include <v4l2++/pixelformats.h>

using namespace std;

namespace v4l2
{
static const map<PixelFormat, PixelFormatInfo> format_info_array = {
	/* YUV packed */
	{ PixelFormat::UYVY, {
				     PixelColorType::YUV,
				     1,
				     { { 16, 2, 1 } },
			     } },
	{ PixelFormat::YUYV, {
				     PixelColorType::YUV,
				     1,
				     { { 16, 2, 1 } },
			     } },
	{ PixelFormat::YVYU, {
				     PixelColorType::YUV,
				     1,
				     { { 16, 2, 1 } },
			     } },
	{ PixelFormat::VYUY, {
				     PixelColorType::YUV,
				     1,
				     { { 16, 2, 1 } },
			     } },
	/* YUV semi-planar */
	{ PixelFormat::NV12, {
				     PixelColorType::YUV,
				     2,
				     { {
					       8,
					       1,
					       1,
				       },
				       { 8, 2, 2 } },
			     } },
	{ PixelFormat::NV21, {
				     PixelColorType::YUV,
				     2,
				     { {
					       8,
					       1,
					       1,
				       },
				       { 8, 2, 2 } },
			     } },
	{ PixelFormat::NV16, {
				     PixelColorType::YUV,
				     2,
				     { {
					       8,
					       1,
					       1,
				       },
				       { 8, 2, 1 } },
			     } },
	{ PixelFormat::NV61, {
				     PixelColorType::YUV,
				     2,
				     { {
					       8,
					       1,
					       1,
				       },
				       { 8, 2, 1 } },
			     } },
	/* RGB16 */
	{ PixelFormat::RGB565, {
				       PixelColorType::RGB,
				       1,
				       { { 16, 1, 1 } },
			       } },
	/* RGB24 */
	{ PixelFormat::RGB888, {
				       PixelColorType::RGB,
				       1,
				       { { 24, 1, 1 } },
			       } },
	/* RGB32 */
	{ PixelFormat::XRGB8888, {
					 PixelColorType::RGB,
					 1,
					 { { 32, 1, 1 } },
				 } },
	{ PixelFormat::SBGGR8, {
					PixelColorType::RAW,
					    1,
					    { { 8, 1, 1 } },
					    } },
	{ PixelFormat::SGBRG8, {
					PixelColorType::RAW,
					    1,
					    { { 8, 1, 1 } },
					    } },
	{ PixelFormat::SGRBG8, {
					PixelColorType::RAW,
					    1,
					    { { 8, 1, 1 } },
					    } },
	{ PixelFormat::SRGGB8, {
					PixelColorType::RAW,
					    1,
					    { { 8, 1, 1 } },
					    } },
	{ PixelFormat::SBGGR12, {
					PixelColorType::RAW,
					1,
					{ { 16, 1, 1 } },
				} },
	{ PixelFormat::SRGGB12, {
					PixelColorType::RAW,
					1,
					{ { 16, 1, 1 } },
				} },
	{ PixelFormat::META_8, {
				       PixelColorType::RGB,
				       1,
				       { { 8, 1, 1 } },
			       } },
	{ PixelFormat::META_16, {
					PixelColorType::RGB,
					1,
					{ { 16, 1, 1 } },
				} },
};

PixelFormat DRMFourCCToPixelFormat(const std::string& fourcc)
{
	// Handle the formats which differ between DRM and V4L2
	if (fourcc == "RG16")
		return PixelFormat::RGB565;
	if (fourcc == "XR24")
		return PixelFormat::XRGB8888;
	if (fourcc == "RG24")
		return PixelFormat::RGB888;

	return FourCCToPixelFormat(fourcc);
}

std::string PixelFormatToDRMFourCC(PixelFormat fmt)
{
	// Handle the formats which differ between DRM and V4L2
	switch (fmt) {
	case PixelFormat::RGB565:
		return "RG16";
	case PixelFormat::XRGB8888:
		return "XR24";
	case PixelFormat::RGB888:
		return "RG24";
	default:
		return PixelFormatToFourCC(fmt);
	}
}

const struct PixelFormatInfo& get_pixel_format_info(PixelFormat format)
{
	if (!format_info_array.count(format))
		throw invalid_argument("v4l2: get_pixel_format_info: Unsupported pixelformat");

	return format_info_array.at(format);
}

} // namespace v4l2
