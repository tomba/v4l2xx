#!/bin/sh

dirs="v4l2++ py"
find $dirs \( -name "*.cpp" -o -name "*.h" \) -exec clang-format -i {} \;
