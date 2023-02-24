#!/usr/bin/python3

import pyv4l2 as v4l2
import pykms

META_LINES = 1

sensor_w = 640
sensor_h = 480
sensor_bus_fmt = v4l2.BusFormat.UYVY8_2X8
sensor_fmt = (sensor_w, sensor_h, sensor_bus_fmt)

vip_slice_out_w = sensor_w
vip_slice_out_h = sensor_h
vip_slice_out_bus_fmt = sensor_bus_fmt
vip_slice_out_fmt = (vip_slice_out_w, vip_slice_out_h, vip_slice_out_bus_fmt)

vip_w = sensor_w
vip_h = sensor_h
vip_pix_fmt = v4l2.PixelFormat.UYVY
vip_fmt = (vip_w, vip_h, vip_pix_fmt)

configurations = {}

OVNAME="ov10635"

#
# Non-MC VIP + OV10635
#
configurations["legacy-vip-ov10635"] = {
	"devices": [
		{
			"fmt": vip_fmt,
			"dev": "/dev/video0",
		},
	],
}

#
# AM5 EVM + VIP + OV10635
#
configurations["vip-ov10635"] = {
	"subdevs": [
		{
			"entity": OVNAME + " 4-0030",
			"pads": [
				{ "pad": 0, "fmt": sensor_fmt },
			],
		},
		{
			"entity": "vip2s0",
			"pads": [
				{ "pad": 0, "fmt": sensor_fmt },
				{ "pad": 2, "fmt": vip_slice_out_fmt },
			],
		},
	],

	"devices": [
		{
			"entity": "VIP 0:0:0",
			"fmt": vip_fmt,
			"dev": "/dev/video0",
		},
	],

	"links": [
#		{ "src": ("ov5640 3-003c", 0), "dst": ("CAMERARX0", 0) },
#		{ "src": ("CAMERARX0", 1), "dst": ("CAL output 0", 0) },
	],
}
