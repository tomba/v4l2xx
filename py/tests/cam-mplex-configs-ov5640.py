#!/usr/bin/python3

import pyv4l2 as v4l2
import pykms

META_LINES = 1

sensor_1_w = 1280
sensor_1_h = 720

PIX_BUS_FMT = v4l2.BusFormat.UYVY8_1X16
PIX_FMT = v4l2.PixelFormat.UYVY

mbus_fmt_pix_1 = (sensor_1_w, sensor_1_h, PIX_BUS_FMT)
mbus_fmt_meta_1 = (sensor_1_w, META_LINES, v4l2.BusFormat.METADATA_16)
fmt_pix_1 = (sensor_1_w, sensor_1_h, PIX_FMT)
fmt_meta_1 = (sensor_1_w, META_LINES, v4l2.PixelFormat.META_16)

configurations = {}

#
# Non-MC OV5640
#
configurations["legacy-ov5640"] = {
	"devices": [
		{
			"fmt": fmt_pix_1,
			"dev": "/dev/video0",
		},
	],
}

#
# AM6 EVM: OV5640
#
configurations["am6-ov5640"] = {
	"subdevs": [
		{
			"entity": "ov5640 3-003c",
			"pads": [
				{ "pad": (0, 0), "fmt": mbus_fmt_pix_1 },
			],
		},
		{
			"entity": "CAMERARX0",
			"pads": [
				{ "pad": (0, 0), "fmt": mbus_fmt_pix_1 },
				{ "pad": (1, 0), "fmt": mbus_fmt_pix_1 },
			],
		},
	],

	"devices": [
		{
			"entity": "CAL output 0",
			"fmt": fmt_pix_1,
			"dev": "/dev/video0",
		},
	],

	"links": [
		{ "src": ("ov5640 3-003c", 0), "dst": ("CAMERARX0", 0) },
		{ "src": ("CAMERARX0", 1), "dst": ("CAL output 0", 0) },
	],
}

#
# J7 EVM: OV5640
#
configurations["j7-ov5640"] = {
	"subdevs": [
		{
			"entity": "ov5640 9-003c",
			"pads": [
				{ "pad": (0, 0), "fmt": mbus_fmt_pix_1 },
			],
		},
		{
			"entity": "cdns_csi2rx.4504000.csi-bridge",
		},
	],

	"devices": [
		{
			"entity": "j721e-csi2rx",
			"fmt": fmt_pix_1,
			"dev": "/dev/video0",
		},
	],

	"links": [
		{ "src": ("ov5640 9-003c", 0), "dst": ("cdns_csi2rx.4504000.csi-bridge", 0) },
		{ "src": ("cdns_csi2rx.4504000.csi-bridge", 1), "dst": ("j721e-csi2rx", 0) },
	],
}

#
# DRA76 EVM: OV5640
#
configurations["dra7-ov5640"] = {
	"subdevs": [
		{
			"entity": "ov5640 4-003c",
			"pads": [
				{ "pad": (0, 0), "fmt": mbus_fmt_pix_1 },
			],
		},
		{
			"entity": "CAMERARX0",
			"pads": [
				{ "pad": (0, 0), "fmt": mbus_fmt_pix_1 },
				{ "pad": (1, 0), "fmt": mbus_fmt_pix_1 },
			],
		},
	],

	"devices": [
		{
			"entity": "CAL output 0",
			"fmt": fmt_pix_1,
			"dev": "/dev/video0",
		},
	],

	"links": [
		{ "src": ("ov5640 4-003c", 0), "dst": ("CAMERARX0", 0) },
		{ "src": ("CAMERARX0", 1), "dst": ("CAL output 0", 0) },
	],
}
