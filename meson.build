project('v4l2++', 'cpp',
    default_options : [
        'cpp_std=c++17',
    ],
    version: '0.0.0',
)

cpp = meson.get_compiler('cpp')
cpp_arguments = []

if (cpp.get_id() == 'gcc' and
    host_machine.cpu_family() == 'arm' and
    cpp.has_argument('-Wno-psabi'))
    cpp_arguments += [
        '-Wno-psabi',
    ]
endif

if cpp.has_argument('-Wno-c99-designator')
    cpp_arguments += [
        '-Wno-c99-designator',
    ]
endif

add_project_arguments(cpp_arguments, language : 'cpp')

link_arguments = []

if get_option('static-libc')
    link_arguments += ['-static-libgcc', '-static-libstdc++']
endif

add_global_link_arguments(link_arguments, language : 'cpp')

common_includes = include_directories('include')

libfmt_dep = dependency('fmt')

subdir('v4l2++')
subdir('py')

summary({
            'Python bindings': pybindings_enabled,
        },
        section : 'Configuration',
        bool_yn : true)
