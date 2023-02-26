[![Build Status](https://github.com/tomba/v4l2xx/actions/workflows/c-cpp.yml/badge.svg)](https://github.com/tomba/v4l2xx/actions/workflows/c-cpp.yml)

# v4l2++ - C++ library for Linux V4L2

v4l2++ is a C++17 library for Linux V4L2. The library is in a quite experimental stage.

Also included are some simple utilities and python bindings.

## Dependencies:

- Python 3.x (for python bindings)

## Build instructions:

To build the Python bindings you need to set up the git-submodule for pybind11:

```
git submodule update --init
```

And to compile:

```
meson build
ninja -C build
```

## Cross compiling instructions:

```
meson build --cross-file=<path-to-meson-cross-file>
ninja -C build
```

Here is my cross file for arm32 (where ${BROOT} is path to my buildroot output dir):

```
[binaries]
c = ['ccache', '${BROOT}/host/bin/arm-buildroot-linux-gnueabihf-gcc']
cpp = ['ccache', '${BROOT}/host/bin/arm-buildroot-linux-gnueabihf-g++']
ar = '${BROOT}/host/bin/arm-buildroot-linux-gnueabihf-ar'
strip = '${BROOT}/host/bin/arm-buildroot-linux-gnueabihf-strip'
pkgconfig = '${BROOT}/host/bin/pkg-config'

[host_machine]
system = 'linux'
cpu_family = 'arm'
cpu = 'arm'
endian = 'little'
```

## Python notes

You can run the python code directly from the build dir by defining PYTHONPATH env variable. For example:

```
PYTHONPATH=build/py py/tests/hpd.py
```
