#pragma once

#include <cstdint>
#include <string>
#include <stdexcept>

namespace v4l2
{

constexpr uint32_t MakeFourCC(const char* fourcc)
{
	return fourcc[0] | (fourcc[1] << 8) | (fourcc[2] << 16) | (fourcc[3] << 24);
}

enum class PixelFormat : uint32_t {
	Undefined = 0,

	NV12 = MakeFourCC("NV12"),
	NV21 = MakeFourCC("NV21"),
	NV16 = MakeFourCC("NV16"),
	NV61 = MakeFourCC("NV61"),

	UYVY = MakeFourCC("UYVY"),
	YUYV = MakeFourCC("YUYV"),
	YVYU = MakeFourCC("YVYU"),
	VYUY = MakeFourCC("VYUY"),

	RGB888 = MakeFourCC("RGB3"),
	XRGB8888 = MakeFourCC("RGB4"),

	RGB332 = MakeFourCC("RGB8"),

	RGB565 = MakeFourCC("RGBP"),

	SBGGR8 = MakeFourCC("BA81"),
	SGBRG8 = MakeFourCC("GBRG"),
	SGRBG8 = MakeFourCC("GRBG"),
	SRGGB8 = MakeFourCC("RGGB"),

	SBGGR12 = MakeFourCC("BG12"),
	SRGGB12 = MakeFourCC("RG12"),

	META_8 = MakeFourCC("ME08"),
	META_16 = MakeFourCC("ME16"),
};

inline PixelFormat FourCCToPixelFormat(const std::string& fourcc)
{
	return (PixelFormat)MakeFourCC(fourcc.c_str());
}

PixelFormat DRMFourCCToPixelFormat(const std::string& fourcc);
std::string PixelFormatToDRMFourCC(PixelFormat fmt);

inline std::string PixelFormatToFourCC(PixelFormat f)
{
	char buf[5] = { (char)(((uint32_t)f >> 0) & 0xff),
			(char)(((uint32_t)f >> 8) & 0xff),
			(char)(((uint32_t)f >> 16) & 0xff),
			(char)(((uint32_t)f >> 24) & 0xff),
			0 };
	return std::string(buf);
}

enum class PixelColorType {
	RGB,
	YUV,
	RAW,
};

struct PixelFormatPlaneInfo {
	uint8_t bitspp;
	uint8_t xsub;
	uint8_t ysub;
};

struct PixelFormatInfo {
	PixelColorType type;
	uint8_t num_planes;
	struct PixelFormatPlaneInfo planes[4];
};

const struct PixelFormatInfo& get_pixel_format_info(PixelFormat format);

} // namespace v4l2
