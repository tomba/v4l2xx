#!/usr/bin/python3

import pyv4l2 as v4l2
import pykms

META_LINES = 1

sensor_1_w = 1280
sensor_1_h = 720

sensor_2_w = 752
sensor_2_h = 480

imx390_w = 1936
imx390_h = 1100
imx390_bus_fmt = v4l2.BusFormat.SRGGB12_1X12
imx390_pix_fmt = v4l2.PixelFormat.SRGGB12

PIX_BUS_FMT = v4l2.BusFormat.UYVY8_1X16
PIX_FMT = v4l2.PixelFormat.UYVY

mbus_fmt_pix_1 = (sensor_1_w, sensor_1_h, PIX_BUS_FMT)
mbus_fmt_meta_1 = (sensor_1_w, META_LINES, v4l2.BusFormat.METADATA_16)
fmt_pix_1 = (sensor_1_w, sensor_1_h, PIX_FMT)
fmt_meta_1 = (sensor_1_w, META_LINES, v4l2.PixelFormat.META_16)

mbus_fmt_pix_2 = (sensor_2_w, sensor_2_h, PIX_BUS_FMT)
mbus_fmt_meta_2 = (sensor_2_w, META_LINES, v4l2.BusFormat.METADATA_16)
fmt_pix_2 = (sensor_2_w, sensor_2_h, PIX_FMT)
fmt_meta_2 = (sensor_2_w, META_LINES, v4l2.PixelFormat.META_16)

mbus_fmt_imx390 = (imx390_w, imx390_h, imx390_bus_fmt)
fmt_pix_imx390 = (imx390_w, imx390_h, imx390_pix_fmt)

mbus_fmt_imx390_meta = (imx390_w, 1, v4l2.BusFormat.METADATA_16)
fmt_pix_imx390_meta = (imx390_w, 1, v4l2.PixelFormat.META_16)

configurations = {}

OVNAME="ov10635"

#
# AM5 EVM + VIP + OV10635
#
configurations["am5-vip"] = {
    "subdevs": [
        {
            "entity": OVNAME + " 4-0030",
            "pads": [
                { "pad": 0, "fmt": (1280, 800, v4l2.BusFormat.UYVY8_2X8) },
            ],
        },
    ],

    "devices": [
        {
            "entity": "VIP 0:0:0",
            "fmt": (1280, 800, v4l2.PixelFormat.UYVY),
            "dev": "/dev/video0",
        },
    ],

    "links": [
        { "src": (OVNAME + " 4-0030", 0), "dst": ("VIP 0:0:0", 0) },
    ],
}


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
                { "pad": (0, 0), "fmt": mbus_fmt_pix_2 },
            ],
        },
        {
            "entity": "CAMERARX0",
            "pads": [
                { "pad": (0, 0), "fmt": mbus_fmt_pix_2 },
                { "pad": (1, 0), "fmt": mbus_fmt_pix_2 },
            ],
        },
    ],

    "devices": [
        {
            "entity": "CAL output 0",
            "fmt": fmt_pix_2,
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

#
# DRA76: UB9060 1 camera, pixel and metadata streams
#
configurations["dra76-ub960-1-cam-meta"] = {
    "subdevs": [
        # cam 1
        {
            "entity": OVNAME + " 5-0030",
            "pads": [
                { "pad": 0, "fmt": mbus_fmt_pix_1 },
            ],
            "routing": [
                { "src": (0, 0), "dst": (0, 0), "flags": [ "source" ] },
                { "src": (0, 1), "dst": (0, 1), "flags": [ "source" ] },
            ],
        },
        # Serializer
        {
            "entity": "ds90ub913a 4-0044",
            "routing": [
                { "src": (0, 0), "dst": (1, 0) },
                { "src": (0, 1), "dst": (1, 1) },
            ],
            "pads": [
                { "pad": (0, 0), "fmt": mbus_fmt_pix_1 },
                { "pad": (1, 0), "fmt": mbus_fmt_pix_1 },
                { "pad": (0, 1), "fmt": mbus_fmt_meta_1 },
                { "pad": (1, 1), "fmt": mbus_fmt_meta_1 },
            ],
        },
        # Deserializer
        {
            "entity": "ds90ub960 4-003d",
            "routing": [
                # cam 1
                { "src": (0, 0), "dst": (4, 0) },
                { "src": (0, 1), "dst": (4, 1) },
            ],
            "pads": [
                # cam 1
                { "pad": (0, 0), "fmt": mbus_fmt_pix_1 },
                { "pad": (0, 1), "fmt": mbus_fmt_meta_1 },
                { "pad": (4, 0), "fmt": mbus_fmt_pix_1 },
                { "pad": (4, 1), "fmt": mbus_fmt_meta_1 },
            ],
        },
        {
            "entity": "CAMERARX0",
            "routing": [
                # cam 1
                { "src": (0, 0), "dst": (1, 0) },
                { "src": (0, 1), "dst": (2, 0) },
            ],
            "pads": [
                # cam 1
                { "pad": (0, 0), "fmt": mbus_fmt_pix_1 },
                { "pad": (0, 1), "fmt": mbus_fmt_meta_1 },
                { "pad": (1, 0), "fmt": mbus_fmt_pix_1 },
                { "pad": (2, 0), "fmt": mbus_fmt_meta_1 },
            ],
        },
    ],

    "devices": [
        # cam 1
        {
            "entity": "CAL output 0",
            "fmt": fmt_pix_1,
            "embedded": False,
            "dev": "/dev/video0",
        },
        {
            "entity": "CAL output 1",
            "fmt": fmt_meta_1,
            "embedded": True,
            "dev": "/dev/video1",
        },
    ],

    "links": [
        { "src": (OVNAME + " 5-0030", 0), "dst": ("ds90ub913a 4-0044", 0) },
        { "src": ("ds90ub913a 4-0044", 1), "dst": ("ds90ub960 4-003d", 0) },
        { "src": ("ds90ub960 4-003d", 4), "dst": ("CAMERARX0", 0) },
        { "src": ("CAMERARX0", 1), "dst": ("CAL output 0", 0) },
        { "src": ("CAMERARX0", 2), "dst": ("CAL output 1", 0) },
    ],
}

#
# DRA76: UB9060 2 cameras, only pixel streams
#
configurations["dra76-ub960-2-cam"] = {
    "subdevs": [
        # Camera 1
        {
            "entity": OVNAME + " 5-0030",
            "pads": [
                { "pad": 0, "fmt": mbus_fmt_pix_1 },
            ],
            "routing": [
                { "src": (0, 0), "dst": (0, 0), "flags": [ "source" ] },
            ],
        },
        # Serializer 1
        {
            "entity": "ds90ub913a 4-0044",
            "routing": [
                { "src": (0, 0), "dst": (1, 0) },
            ],
            "pads": [
                { "pad": (0, 0), "fmt": mbus_fmt_pix_1 },
                { "pad": (1, 0), "fmt": mbus_fmt_pix_1 },
            ],
        },
        # Camera 2
        {
            "entity": OVNAME + " 6-0030",
            "pads": [
                { "pad": 0, "fmt": mbus_fmt_pix_2 },
            ],
            "routing": [
                { "src": (0, 0), "dst": (0, 0), "flags": [ "source" ] },
            ],
        },
        # Serializer 2
        {
            "entity": "ds90ub913a 4-0045",
            "routing": [
                { "src": (0, 0), "dst": (1, 0) },
            ],
            "pads": [
                { "pad": (0, 0), "fmt": mbus_fmt_pix_2 },
                { "pad": (1, 0), "fmt": mbus_fmt_pix_2 },
            ],
        },
        # Deserializer
        {
            "entity": "ds90ub960 4-003d",
            "routing": [
                # Camera 1
                { "src": (0, 0), "dst": (4, 0) },
                # Camera 2
                { "src": (1, 0), "dst": (4, 1) },
            ],
            "pads": [
                # Camera 1
                { "pad": (0, 0), "fmt": mbus_fmt_pix_1 },
                { "pad": (4, 0), "fmt": mbus_fmt_pix_1 },
                # Camera 2
                { "pad": (1, 0), "fmt": mbus_fmt_pix_2 },
                { "pad": (4, 1), "fmt": mbus_fmt_pix_2 },
            ],
        },
        # CSI-2 RX
        {
            "entity": "CAMERARX0",
            "routing": [
                # cam 1
                { "src": (0, 0), "dst": (1, 0) },
                # cam 2
                { "src": (0, 1), "dst": (2, 0) },
            ],
            "pads": [
                # cam 1
                { "pad": (0, 0), "fmt": mbus_fmt_pix_1 },
                { "pad": (1, 0), "fmt": mbus_fmt_pix_1 },
                # cam 2
                { "pad": (0, 1), "fmt": mbus_fmt_pix_2 },
                { "pad": (2, 0), "fmt": mbus_fmt_pix_2 },
            ],
        },
    ],

    "devices": [
        # cam 1
        {
            "entity": "CAL output 0",
            "fmt": fmt_pix_1,
            "embedded": False,
            "dev": "/dev/video0",
        },
        # cam 2
        {
            "entity": "CAL output 1",
            "fmt": fmt_pix_2,
            "embedded": False,
            "dev": "/dev/video1",
        },
    ],

    "links": [
        { "src": (OVNAME + " 5-0030", 0), "dst": ("ds90ub913a 4-0044", 0) },
        { "src": ("ds90ub913a 4-0044", 1), "dst": ("ds90ub960 4-003d", 0) },
        { "src": (OVNAME + " 6-0030", 0), "dst": ("ds90ub913a 4-0045", 0) },
        { "src": ("ds90ub913a 4-0045", 1), "dst": ("ds90ub960 4-003d", 1) },
        { "src": ("ds90ub960 4-003d", 4), "dst": ("CAMERARX0", 0) },
        { "src": ("CAMERARX0", 1), "dst": ("CAL output 0", 0) },
        { "src": ("CAMERARX0", 2), "dst": ("CAL output 1", 0) },
    ],
}

#
# DRA76: UB9060 2 cameras, pixel and metadata streams
#
configurations["dra76-ub960-2-cam-meta"] = {
    "subdevs": [
        # Camera 1
        {
            "entity": OVNAME + " 5-0030",
            "routing": [
                { "src": (0, 0), "dst": (0, 0), "flags": [ "source" ] },
                { "src": (0, 1), "dst": (0, 1), "flags": [ "source" ] },
            ],
            "pads": [
                { "pad": (0, 0), "fmt": mbus_fmt_pix_1 },
            ],
        },
        # Serializer 1
        {
            "entity": "ds90ub913a 4-0044",
            "routing": [
                { "src": (0, 0), "dst": (1, 0) },
                { "src": (0, 1), "dst": (1, 1) },
            ],
            "pads": [
                { "pad": (0, 0), "fmt": mbus_fmt_pix_1 },
                { "pad": (1, 0), "fmt": mbus_fmt_pix_1 },
                { "pad": (0, 1), "fmt": mbus_fmt_meta_1 },
                { "pad": (1, 1), "fmt": mbus_fmt_meta_1 },
            ],
        },
        # Camera 2
        {
            "entity": OVNAME + " 6-0030",
            "routing": [
                { "src": (0, 0), "dst": (0, 0), "flags": [ "source" ] },
                { "src": (0, 1), "dst": (0, 1), "flags": [ "source" ] },
            ],
            "pads": [
                { "pad": 0, "fmt": mbus_fmt_pix_2 },
            ],
        },
        # Serializer 2
        {
            "entity": "ds90ub913a 4-0045",
            "routing": [
                { "src": (0, 0), "dst": (1, 0) },
                { "src": (0, 1), "dst": (1, 1) },
            ],
            "pads": [
                { "pad": (0, 0), "fmt": mbus_fmt_pix_2 },
                { "pad": (1, 0), "fmt": mbus_fmt_pix_2 },
                { "pad": (0, 1), "fmt": mbus_fmt_meta_2 },
                { "pad": (1, 1), "fmt": mbus_fmt_meta_2 },
            ],
        },
        # Deserializer
        {
            "entity": "ds90ub960 4-003d",
            "routing": [
                # Camera 1
                { "src": (0, 0), "dst": (4, 0) },
                { "src": (0, 1), "dst": (4, 1) },
                # Camera 2
                { "src": (1, 0), "dst": (4, 2) },
                { "src": (1, 1), "dst": (4, 3) },
            ],
            "pads": [
                # Camera 1
                { "pad": (0, 0), "fmt": mbus_fmt_pix_1 },
                { "pad": (0, 1), "fmt": mbus_fmt_meta_1 },
                { "pad": (4, 0), "fmt": mbus_fmt_pix_1 },
                { "pad": (4, 1), "fmt": mbus_fmt_meta_1 },
                # Camera 2
                { "pad": (1, 0), "fmt": mbus_fmt_pix_2 },
                { "pad": (1, 1), "fmt": mbus_fmt_meta_2 },
                { "pad": (4, 2), "fmt": mbus_fmt_pix_2 },
                { "pad": (4, 3), "fmt": mbus_fmt_meta_2 },
            ],
        },
        # CSI-2 RX
        {
            "entity": "CAMERARX0",
            "routing": [
                # cam 1
                { "src": (0, 0), "dst": (1, 0) },
                { "src": (0, 1), "dst": (2, 0) },
                # cam 2
                { "src": (0, 2), "dst": (3, 0) },
                { "src": (0, 3), "dst": (4, 0) },
            ],
            "pads": [
                # cam 1
                { "pad": (0, 0), "fmt": mbus_fmt_pix_1 },
                { "pad": (0, 1), "fmt": mbus_fmt_meta_1 },
                { "pad": (1, 0), "fmt": mbus_fmt_pix_1 },
                { "pad": (2, 0), "fmt": mbus_fmt_meta_1 },
                # cam 2
                { "pad": (0, 2), "fmt": mbus_fmt_pix_2 },
                { "pad": (0, 3), "fmt": mbus_fmt_meta_2 },
                { "pad": (3, 0), "fmt": mbus_fmt_pix_2 },
                { "pad": (4, 0), "fmt": mbus_fmt_meta_2 },
            ],
        },
    ],

    "devices": [
        # cam 1
        {
            "entity": "CAL output 0",
            "fmt": fmt_pix_1,
            "embedded": False,
            "dev": "/dev/video0",
        },
        {
            "entity": "CAL output 1",
            "fmt": fmt_meta_1,
            "embedded": True,
            "dev": "/dev/video1",
        },
        # cam 2
        {
            "entity": "CAL output 2",
            "fmt": fmt_pix_2,
            "embedded": False,
            "dev": "/dev/video2",
        },
        {
            "entity": "CAL output 3",
            "fmt": fmt_meta_2,
            "embedded": True,
            "dev": "/dev/video3",
        },
    ],

    "links": [
        { "src": (OVNAME + " 5-0030", 0), "dst": ("ds90ub913a 4-0044", 0) },
        { "src": ("ds90ub913a 4-0044", 1), "dst": ("ds90ub960 4-003d", 0) },
        { "src": (OVNAME + " 6-0030", 0), "dst": ("ds90ub913a 4-0045", 0) },
        { "src": ("ds90ub913a 4-0045", 1), "dst": ("ds90ub960 4-003d", 1) },
        { "src": ("ds90ub960 4-003d", 4), "dst": ("CAMERARX0", 0) },
        { "src": ("CAMERARX0", 1), "dst": ("CAL output 0", 0) },
        { "src": ("CAMERARX0", 2), "dst": ("CAL output 1", 0) },
        { "src": ("CAMERARX0", 3), "dst": ("CAL output 2", 0) },
        { "src": ("CAMERARX0", 4), "dst": ("CAL output 3", 0) },
    ],
}

#
# AM6: UB9060 2 cameras, only pixel streams
#
configurations["am6-ub960-2-cam"] = {
    "subdevs": [
        # cam 1
        {
            "entity": OVNAME + " 6-0030",
            "pads": [
                { "pad": 0, "fmt": mbus_fmt_pix_1 },
            ],
        },
        {
            "entity": "ds90ub913a 3-0044",
        },
        # cam 2
        {
            "entity": OVNAME + " 7-0030",
            "pads": [
                { "pad": 0, "fmt": mbus_fmt_pix_2 },
            ],
        },
        {
            "entity": "ds90ub913a 3-0045",
        },
        # deser
        {
            "entity": "ds90ub960 3-003d",
            "routing": [
                # cam 1
                { "src": (0, 0), "dst": (4, 0) },
                # cam 2
                { "src": (1, 0), "dst": (4, 1) },
            ],
            "pads": [
                # cam 1
                { "pad": (0, 0), "fmt": mbus_fmt_pix_1 },
                { "pad": (4, 0), "fmt": mbus_fmt_pix_1 },
                # cam 2
                { "pad": (1, 0), "fmt": mbus_fmt_pix_2 },
                { "pad": (4, 1), "fmt": mbus_fmt_pix_2 },
            ],
        },
        {
            "entity": "CAMERARX0",
            "routing": [
                # cam 1
                { "src": (0, 0), "dst": (1, 0) },
                { "src": (0, 1), "dst": (2, 0) },
                # cam 2
                { "src": (0, 2), "dst": (3, 0) },
                { "src": (0, 3), "dst": (4, 0) },
            ],
            "pads": [
                # cam 1
                { "pad": (0, 0), "fmt": mbus_fmt_pix_1 },
                { "pad": (0, 1), "fmt": mbus_fmt_meta_1 },
                { "pad": (1, 0), "fmt": mbus_fmt_pix_1 },
                { "pad": (2, 0), "fmt": mbus_fmt_meta_1 },
                # cam 2
                { "pad": (0, 2), "fmt": mbus_fmt_pix_2 },
                { "pad": (0, 3), "fmt": mbus_fmt_meta_2 },
                { "pad": (3, 0), "fmt": mbus_fmt_pix_2 },
                { "pad": (4, 0), "fmt": mbus_fmt_meta_2 },
            ],
        },
    ],

    "devices": [
        {
            "entity": "CAL output 0",
            "fmt": fmt_pix_1,
            "embedded": False,
            "dev": "/dev/video0",
        },
        {
            "entity": "CAL output 1",
            "fmt": fmt_pix_2,
            "embedded": False,
            "dev": "/dev/video1",
        },
    ],

    "links": [
        { "src": (OVNAME + " 6-0030", 0), "dst": ("ds90ub913a 3-0044", 0) },
        { "src": ("ds90ub913a 3-0044", 1), "dst": ("ds90ub960 3-003d", 0) },
        { "src": (OVNAME + " 7-0030", 0), "dst": ("ds90ub913a 3-0045", 0) },
        { "src": ("ds90ub913a 3-0045", 1), "dst": ("ds90ub960 3-003d", 1) },
        { "src": ("ds90ub960 3-003d", 4), "dst": ("CAMERARX0", 0) },
        { "src": ("CAMERARX0", 1), "dst": ("CAL output 0", 0) },
        { "src": ("CAMERARX0", 2), "dst": ("CAL output 1", 0) },
    ],
}



#
# DRA76: UB9060, 2xUB913, 1xUB953, only pixel streams
#
configurations["dra76-ub960-3-cam"] = {
    "subdevs": [
        # Camera 1
        {
            "entity": OVNAME + " 5-0030",
            "pads": [
                { "pad": 0, "fmt": mbus_fmt_pix_1 },
            ],
            "routing": [
                { "src": (0, 0), "dst": (0, 0), "flags": [ "source" ] },
            ],
        },
        # Serializer 1
        {
            "entity": "ds90ub913a 4-0044",
            "routing": [
                { "src": (0, 0), "dst": (1, 0) },
            ],
            "pads": [
                { "pad": (0, 0), "fmt": mbus_fmt_pix_1 },
                { "pad": (1, 0), "fmt": mbus_fmt_pix_1 },
            ],
        },

        # Camera 2
        {
            "entity": OVNAME + " 6-0030",
            "pads": [
                { "pad": 0, "fmt": mbus_fmt_pix_2 },
            ],
            "routing": [
                { "src": (0, 0), "dst": (0, 0), "flags": [ "source" ] },
            ],
        },
        # Serializer 2
        {
            "entity": "ds90ub913a 4-0045",
            "routing": [
                { "src": (0, 0), "dst": (1, 0) },
            ],
            "pads": [
                { "pad": (0, 0), "fmt": mbus_fmt_pix_2 },
                { "pad": (1, 0), "fmt": mbus_fmt_pix_2 },
            ],
        },

        # Camera 3
        {
            "entity": "imx390 7-0021",
            "pads": [
                { "pad": 0, "fmt": mbus_fmt_imx390 },
            ],
            "routing": [
                { "src": (0, 0), "dst": (0, 0), "flags": [ "source" ] },
            ],
        },
        # Serializer 3
        {
            "entity": "ds90ub953 4-0046",
            "routing": [
                { "src": (0, 0), "dst": (1, 0) },
            ],
            "pads": [
                { "pad": (0, 0), "fmt": mbus_fmt_imx390 },
                { "pad": (1, 0), "fmt": mbus_fmt_imx390 },
            ],
        },
        # Deserializer
        {
            "entity": "ds90ub960 4-003d",
            "routing": [
                # Camera 1
                { "src": (0, 0), "dst": (4, 0) },
                # Camera 2
                { "src": (1, 0), "dst": (4, 1) },
                # Camera 3
                { "src": (2, 0), "dst": (4, 2) },
            ],
            "pads": [
                # Camera 1
                { "pad": (0, 0), "fmt": mbus_fmt_pix_1 },
                { "pad": (4, 0), "fmt": mbus_fmt_pix_1 },
                # Camera 2
                { "pad": (1, 0), "fmt": mbus_fmt_pix_2 },
                { "pad": (4, 1), "fmt": mbus_fmt_pix_2 },
                # Camera 3
                { "pad": (2, 0), "fmt": mbus_fmt_imx390 },
                { "pad": (4, 2), "fmt": mbus_fmt_imx390 },
            ],
        },
        # CSI-2 RX
        {
            "entity": "CAMERARX0",
            "routing": [
                # cam 1
                { "src": (0, 0), "dst": (1, 0) },
                # cam 2
                { "src": (0, 1), "dst": (2, 0) },
                # cam 3
                { "src": (0, 2), "dst": (3, 0) },
            ],
            "pads": [
                # cam 1
                { "pad": (0, 0), "fmt": mbus_fmt_pix_1 },
                { "pad": (1, 0), "fmt": mbus_fmt_pix_1 },
                # cam 2
                { "pad": (0, 1), "fmt": mbus_fmt_pix_2 },
                { "pad": (2, 0), "fmt": mbus_fmt_pix_2 },
                # cam 3
                { "pad": (0, 2), "fmt": mbus_fmt_imx390 },
                { "pad": (3, 0), "fmt": mbus_fmt_imx390 },
            ],
        },
    ],

    "devices": [
        # cam 1
        {
            "entity": "CAL output 0",
            "fmt": fmt_pix_1,
            "embedded": False,
            "dev": "/dev/video0",
        },
        # cam 2
        {
            "entity": "CAL output 1",
            "fmt": fmt_pix_2,
            "embedded": False,
            "dev": "/dev/video1",
        },
        # cam 2
        {
            "entity": "CAL output 2",
            "fmt": fmt_pix_imx390,
            "embedded": False,
            "dev": "/dev/video2",
        },
    ],

    "links": [
        { "src": (OVNAME + " 5-0030", 0), "dst": ("ds90ub913a 4-0044", 0) },
        { "src": ("ds90ub913a 4-0044", 1), "dst": ("ds90ub960 4-003d", 0) },
        { "src": (OVNAME + " 6-0030", 0), "dst": ("ds90ub913a 4-0045", 0) },
        { "src": ("ds90ub913a 4-0045", 1), "dst": ("ds90ub960 4-003d", 1) },
        { "src": ("imx390 7-0021", 0), "dst": ("ds90ub953 4-0046", 0) },
        { "src": ("ds90ub953 4-0046", 1), "dst": ("ds90ub960 4-003d", 2) },
        { "src": ("ds90ub960 4-003d", 4), "dst": ("CAMERARX0", 0) },
        { "src": ("CAMERARX0", 1), "dst": ("CAL output 0", 0) },
        { "src": ("CAMERARX0", 2), "dst": ("CAL output 1", 0) },
        { "src": ("CAMERARX0", 3), "dst": ("CAL output 2", 0) },
    ],
}


#
# DRA76: UB9060 ov1063x on port 0
#
configurations["dra76-ub960-ov10635.0-pixel"] = {
    "subdevs": [
        # Camera
        {
            "entity": OVNAME + " 5-0030",
            "pads": [
                { "pad": 0, "fmt": mbus_fmt_pix_1 },
            ],
            "routing": [
                { "src": (0, 0), "dst": (0, 0), "flags": [ "source" ] },
            ],
        },
        # Serializer
        {
            "entity": "ds90ub913a 4-0044",
            "routing": [
                { "src": (0, 0), "dst": (1, 0) },
            ],
            "pads": [
                { "pad": (0, 0), "fmt": mbus_fmt_pix_1 },
                { "pad": (1, 0), "fmt": mbus_fmt_pix_1 },
            ],
        },
        # Deserializer
        {
            "entity": "ds90ub960 4-003d",
            "routing": [
                { "src": (0, 0), "dst": (4, 0) },
            ],
            "pads": [
                { "pad": (0, 0), "fmt": mbus_fmt_pix_1 },
                { "pad": (4, 0), "fmt": mbus_fmt_pix_1 },
            ],
        },
        # CSI-2 RX
        {
            "entity": "CAMERARX0",
            "routing": [
                { "src": (0, 0), "dst": (1, 0) },
            ],
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
            "embedded": False,
            "dev": "/dev/video0",
        },
    ],

    "links": [
        { "src": (OVNAME + " 5-0030", 0), "dst": ("ds90ub913a 4-0044", 0) },
        { "src": ("ds90ub913a 4-0044", 1), "dst": ("ds90ub960 4-003d", 0) },
        { "src": ("ds90ub960 4-003d", 4), "dst": ("CAMERARX0", 0) },
        { "src": ("CAMERARX0", 1), "dst": ("CAL output 0", 0) },
    ],
}

#
# DRA76: UB9060 ov1063x metadata on port 0
#
configurations["dra76-ub960-ov10635.0-meta"] = {
    "subdevs": [
        # Camera
        {
            "entity": OVNAME + " 5-0030",
            "routing": [
                { "src": (0, 1), "dst": (0, 1), "flags": [ "source" ] },
            ],
        },
        # Serializer
        {
            "entity": "ds90ub913a 4-0044",
            "routing": [
                { "src": (0, 1), "dst": (1, 1) },
            ],
            "pads": [
                { "pad": (0, 1), "fmt": mbus_fmt_meta_1 },
                { "pad": (1, 1), "fmt": mbus_fmt_meta_1 },
            ],
        },
        # Deserializer
        {
            "entity": "ds90ub960 4-003d",
            "routing": [
                { "src": (0, 1), "dst": (4, 4) },
            ],
            "pads": [
                { "pad": (0, 1), "fmt": mbus_fmt_meta_1 },
                { "pad": (4, 4), "fmt": mbus_fmt_meta_1 },
            ],
        },
        # CSI-2 RX
        {
            "entity": "CAMERARX0",
            "routing": [
                { "src": (0, 4), "dst": (5, 0) },
            ],
            "pads": [
                { "pad": (0, 4), "fmt": mbus_fmt_meta_1 },
                { "pad": (5, 0), "fmt": mbus_fmt_meta_1 },
            ],
        },
    ],

    "devices": [
        {
            "entity": "CAL output 4",
            "fmt": fmt_meta_1,
            "embedded": True,
            "dev": "/dev/video4",
            "display": False,
        },
    ],

    "links": [
        { "src": (OVNAME + " 5-0030", 0), "dst": ("ds90ub913a 4-0044", 0) },
        { "src": ("ds90ub913a 4-0044", 1), "dst": ("ds90ub960 4-003d", 0) },
        { "src": ("ds90ub960 4-003d", 4), "dst": ("CAMERARX0", 0) },
        { "src": ("CAMERARX0", 5), "dst": ("CAL output 4", 0) },
    ],
}

#
# DRA76: UB9060 ov1063x on port 1
#
configurations["dra76-ub960-ov10635.1-pixel"] = {
    "subdevs": [
        # Camera
        {
            "entity": OVNAME + " 6-0030",
            "pads": [
                { "pad": 0, "fmt": mbus_fmt_pix_1 },
            ],
            "routing": [
                { "src": (0, 0), "dst": (0, 0), "flags": [ "source" ] },
            ],
        },
        # Serializer
        {
            "entity": "ds90ub913a 4-0045",
            "routing": [
                { "src": (0, 0), "dst": (1, 0) },
            ],
            "pads": [
                { "pad": (0, 0), "fmt": mbus_fmt_pix_1 },
                { "pad": (1, 0), "fmt": mbus_fmt_pix_1 },
            ],
        },
        # Deserializer
        {
            "entity": "ds90ub960 4-003d",
            "routing": [
                { "src": (1, 0), "dst": (4, 1) },
            ],
            "pads": [
                { "pad": (1, 0), "fmt": mbus_fmt_pix_1 },
                { "pad": (4, 1), "fmt": mbus_fmt_pix_1 },
            ],
        },
        # CSI-2 RX
        {
            "entity": "CAMERARX0",
            "routing": [
                { "src": (0, 1), "dst": (2, 0) },
            ],
            "pads": [
                { "pad": (0, 1), "fmt": mbus_fmt_pix_1 },
                { "pad": (2, 0), "fmt": mbus_fmt_pix_1 },
            ],
        },
    ],

    "devices": [
        {
            "entity": "CAL output 1",
            "fmt": fmt_pix_1,
            "embedded": False,
            "dev": "/dev/video1",
        },
    ],

    "links": [
        { "src": (OVNAME + " 6-0030", 0), "dst": ("ds90ub913a 4-0045", 0) },
        { "src": ("ds90ub913a 4-0045", 1), "dst": ("ds90ub960 4-003d", 1) },
        { "src": ("ds90ub960 4-003d", 4), "dst": ("CAMERARX0", 0) },
        { "src": ("CAMERARX0", 2), "dst": ("CAL output 1", 0) },
    ],
}

#
# DRA76: UB9060 ov1063x metadata on port 1
#
configurations["dra76-ub960-ov10635.1-meta"] = {
    "subdevs": [
        # Camera
        {
            "entity": OVNAME + " 6-0030",
            "routing": [
                { "src": (0, 1), "dst": (0, 1), "flags": [ "source" ] },
            ],
        },
        # Serializer
        {
            "entity": "ds90ub913a 4-0045",
            "routing": [
                { "src": (0, 1), "dst": (1, 1) },
            ],
            "pads": [
                { "pad": (0, 1), "fmt": mbus_fmt_meta_1 },
                { "pad": (1, 1), "fmt": mbus_fmt_meta_1 },
            ],
        },
        # Deserializer
        {
            "entity": "ds90ub960 4-003d",
            "routing": [
                { "src": (1, 1), "dst": (4, 5) },
            ],
            "pads": [
                { "pad": (1, 1), "fmt": mbus_fmt_meta_1 },
                { "pad": (4, 5), "fmt": mbus_fmt_meta_1 },
            ],
        },
        # CSI-2 RX
        {
            "entity": "CAMERARX0",
            "routing": [
                { "src": (0, 5), "dst": (6, 0) },
            ],
            "pads": [
                { "pad": (0, 5), "fmt": mbus_fmt_meta_1 },
                { "pad": (6, 0), "fmt": mbus_fmt_meta_1 },
            ],
        },
    ],

    "devices": [
        {
            "entity": "CAL output 5",
            "fmt": fmt_meta_1,
            "embedded": True,
            "dev": "/dev/video5",
            "display": False,
        },
    ],

    "links": [
        { "src": (OVNAME + " 6-0030", 0), "dst": ("ds90ub913a 4-0045", 0) },
        { "src": ("ds90ub913a 4-0045", 1), "dst": ("ds90ub960 4-003d", 1) },
        { "src": ("ds90ub960 4-003d", 4), "dst": ("CAMERARX0", 0) },
        { "src": ("CAMERARX0", 6), "dst": ("CAL output 5", 0) },
    ],
}


def gen_imx390_pixel(port):
    sensor_ent = f"imx390 {port + 5}-0021"
    ser_ent = f"ds90ub953 4-004{4 + port}"

    return {
        "subdevs": [
            # Camera
            {
                "entity": sensor_ent,
                "pads": [
                    { "pad": (0, 0), "fmt": mbus_fmt_imx390 },
                ],
                "routing": [
                   { "src": (0, 0), "dst": (0, 0), "flags": [ "source" ] },
                ],
            },
            # Serializer
            {
                "entity": ser_ent,
                "routing": [
                    { "src": (0, 0), "dst": (1, 0) },
                ],
                "pads": [
                    { "pad": (0, 0), "fmt": mbus_fmt_imx390 },
                    { "pad": (1, 0), "fmt": mbus_fmt_imx390 },
                ],
            },
            # Deserializer
            {
                "entity": "ds90ub960 4-003d",
                "routing": [
                    { "src": (port, 0), "dst": (4, port) },
                ],
                "pads": [
                    { "pad": (port, 0), "fmt": mbus_fmt_imx390 },
                    { "pad": (4, port), "fmt": mbus_fmt_imx390 },
                ],
            },
            # CSI-2 RX
            {
                "entity": "CAMERARX0",
                "routing": [
                    { "src": (0, port), "dst": (1 + port, 0) },
                ],
                "pads": [
                    { "pad": (0, port), "fmt": mbus_fmt_imx390 },
                    { "pad": (1 + port, 0), "fmt": mbus_fmt_imx390 },
                ],
            },
        ],

        "devices": [
            {
                "entity": f"CAL output {port}",
                "fmt": fmt_pix_imx390,
                "embedded": False,
                "dev": f"/dev/video{port}",
                "dra-plane-hack": False,
                "kms-fourcc": pykms.PixelFormat.RGB565,
            },
        ],

        "links": [
            { "src": (sensor_ent, 0), "dst": (ser_ent, 0) },
            { "src": (ser_ent, 1), "dst": ("ds90ub960 4-003d", port) },
            { "src": ("ds90ub960 4-003d", 4), "dst": ("CAMERARX0", 0) },
            { "src": ("CAMERARX0", 1 + port), "dst": (f"CAL output {port}", 0) },
        ],
    }

def gen_imx390_meta(port):
    sensor_ent = f"imx390 {port + 5}-0021"
    ser_ent = f"ds90ub953 4-004{4 + port}"

    return {
        "subdevs": [
            # Camera
            {
                "entity": sensor_ent,
                "pads": [
                    { "pad": (0, 1), "fmt": mbus_fmt_imx390_meta },
                ],
                "routing": [
                   { "src": (0, 1), "dst": (0, 1), "flags": [ "source" ] },
                ],
            },
            # Serializer
            {
                "entity": ser_ent,
                "routing": [
                    { "src": (0, 1), "dst": (1, 1) },
                ],
                "pads": [
                    { "pad": (0, 1), "fmt": mbus_fmt_imx390_meta },
                    { "pad": (1, 1), "fmt": mbus_fmt_imx390_meta },
                ],
            },
            # Deserializer
            {
                "entity": "ds90ub960 4-003d",
                "routing": [
                    { "src": (port, 1), "dst": (4, port + 4) },
                ],
                "pads": [
                    { "pad": (port, 1), "fmt": mbus_fmt_imx390_meta },
                    { "pad": (4, port + 4), "fmt": mbus_fmt_imx390_meta },
                ],
            },
            # CSI-2 RX
            {
                "entity": "CAMERARX0",
                "routing": [
                    { "src": (0, port + 4), "dst": (1 + port + 4, 0) },
                ],
                "pads": [
                    { "pad": (0, port + 4), "fmt": mbus_fmt_imx390_meta },
                    { "pad": (1 + port + 4, 0), "fmt": mbus_fmt_imx390_meta },
                ],
            },
        ],

        "devices": [
            {
                "entity": f"CAL output {port + 4}",
                "fmt": fmt_pix_imx390_meta,
                "embedded": True,
                "dev": f"/dev/video{port + 4}",
                "display": False,
            },
        ],

        "links": [
            { "src": (sensor_ent, 0), "dst": (ser_ent, 0) },
            { "src": (ser_ent, 1), "dst": ("ds90ub960 4-003d", port) },
            { "src": ("ds90ub960 4-003d", 4), "dst": ("CAMERARX0", 0) },
            { "src": ("CAMERARX0", 1 + port + 4), "dst": (f"CAL output {port + 4}", 0) },
        ],
    }

configurations["dra76-ub960-imx390.0-pixel"] = gen_imx390_pixel(0)
configurations["dra76-ub960-imx390.1-pixel"] = gen_imx390_pixel(1)
configurations["dra76-ub960-imx390.2-pixel"] = gen_imx390_pixel(2)
configurations["dra76-ub960-imx390.3-pixel"] = gen_imx390_pixel(3)

configurations["dra76-ub960-imx390.0-meta"] = gen_imx390_meta(0)
configurations["dra76-ub960-imx390.1-meta"] = gen_imx390_meta(1)
configurations["dra76-ub960-imx390.2-meta"] = gen_imx390_meta(2)
configurations["dra76-ub960-imx390.3-meta"] = gen_imx390_meta(3)












def gen_ov10635_pixel(port):
    sensor_ent = OVNAME + f" {port + 5}-0030"
    ser_ent = f"ds90ub913a 4-004{4 + port}"

    fmt_1 = (1280, 720, v4l2.BusFormat.UYVY8_2X8)
    fmt_2 = (1280, 720, v4l2.BusFormat.UYVY8_1X16)

    return {
        "subdevs": [
            # Camera
            {
                "entity": sensor_ent,
                "pads": [
                    { "pad": 0, "fmt": fmt_1 },
                ],
                "routing": [
                    { "src": (0, 0), "dst": (0, 0), "flags": [ "source" ] },
                ],
            },
            # Serializer
            {
                "entity": ser_ent,
                "routing": [
                    { "src": (0, 0), "dst": (1, 0) },
                ],
                "pads": [
                    { "pad": (0, 0), "fmt": fmt_1 },
                    { "pad": (1, 0), "fmt": fmt_2 },
                ],
            },
            # Deserializer
            {
                "entity": "ds90ub960 4-003d",
                "routing": [
                    { "src": (port, 0), "dst": (4, port) },
                ],
                "pads": [
                    { "pad": (port, 0), "fmt": fmt_2 },
                    { "pad": (4, port), "fmt": fmt_2 },
                ],
            },
            # CSI-2 RX
            {
                "entity": "CAMERARX0",
                "routing": [
                    { "src": (0, port), "dst": (1 + port, 0) },
                ],
                "pads": [
                    { "pad": (0, port), "fmt": fmt_2 },
                    { "pad": (1 + port, 0), "fmt": fmt_2 },
                ],
            },
        ],

        "devices": [
            {
                "entity": f"CAL output {port}",
                "fmt": fmt_pix_1,
                "embedded": False,
                "dev": f"/dev/video{port}",
            },
        ],

        "links": [
            { "src": (sensor_ent, 0), "dst": (ser_ent, 0) },
            { "src": (ser_ent, 1), "dst": ("ds90ub960 4-003d", port) },
            { "src": ("ds90ub960 4-003d", 4), "dst": ("CAMERARX0", 0) },
            { "src": ("CAMERARX0", 1 + port), "dst": (f"CAL output {port}", 0) },
        ],
    }


def gen_ov10635_meta(port):
    sensor_ent = OVNAME + f" {port + 5}-0030"
    ser_ent = f"ds90ub913a 4-004{4 + port}"

    return {
        "subdevs": [
            # Camera
            {
                "entity": sensor_ent,
                "routing": [
                   { "src": (0, 1), "dst": (0, 1), "flags": [ "source" ] },
                ],
            },
            # Serializer
            {
                "entity": ser_ent,
                "routing": [
                    { "src": (0, 1), "dst": (1, 1) },
                ],
                "pads": [
                    { "pad": (0, 1), "fmt": mbus_fmt_meta_1 },
                    { "pad": (1, 1), "fmt": mbus_fmt_meta_1 },
                ],
            },
            # Deserializer
            {
                "entity": "ds90ub960 4-003d",
                "routing": [
                    { "src": (port, 1), "dst": (4, port + 4) },
                ],
                "pads": [
                    { "pad": (port, 1), "fmt": mbus_fmt_meta_1 },
                    { "pad": (4, port + 4), "fmt": mbus_fmt_meta_1 },
                ],
            },
            # CSI-2 RX
            {
                "entity": "CAMERARX0",
                "routing": [
                    { "src": (0, port + 4), "dst": (1 + port + 4, 0) },
                ],
                "pads": [
                    { "pad": (0, port + 4), "fmt": mbus_fmt_meta_1 },
                    { "pad": (1 + port + 4, 0), "fmt": mbus_fmt_meta_1 },
                ],
            },
        ],

        "devices": [
            {
                "entity": f"CAL output {port + 4}",
                "fmt": fmt_meta_1,
                "embedded": True,
                "dev": f"/dev/video{port + 4}",
                "display": False,
            },
        ],

        "links": [
            { "src": (sensor_ent, 0), "dst": (ser_ent, 0) },
            { "src": (ser_ent, 1), "dst": ("ds90ub960 4-003d", port) },
            { "src": ("ds90ub960 4-003d", 4), "dst": ("CAMERARX0", 0) },
            { "src": ("CAMERARX0", 1 + port + 4), "dst": (f"CAL output {port + 4}", 0) },
        ],
    }



configurations["dra76-ub960-ov10635.0-pixel"] = gen_ov10635_pixel(0)
configurations["dra76-ub960-ov10635.1-pixel"] = gen_ov10635_pixel(1)
configurations["dra76-ub960-ov10635.2-pixel"] = gen_ov10635_pixel(2)
configurations["dra76-ub960-ov10635.3-pixel"] = gen_ov10635_pixel(3)

configurations["dra76-ub960-ov10635.0-meta"] = gen_ov10635_meta(0)
configurations["dra76-ub960-ov10635.1-meta"] = gen_ov10635_meta(1)
configurations["dra76-ub960-ov10635.2-meta"] = gen_ov10635_meta(2)
configurations["dra76-ub960-ov10635.3-meta"] = gen_ov10635_meta(3)
