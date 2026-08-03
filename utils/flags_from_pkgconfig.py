import sys

def flags_from_pkgconfig(libs):
    r"""Return compiler line flags for FFI.set_source based on pkg-config output

    Usage
        ...
        ffibuilder.set_source("_foo", pkgconfig = ["libfoo", "libbar >= 1.8.3"])

    If pkg-config is installed on build machine, then arguments include_dirs,
    library_dirs, libraries, define_macros, extra_compile_args and
    extra_link_args are extended with an output of pkg-config for libfoo and
    libbar.

    Raises PkgConfigError in case the pkg-config call fails.
    """

    def get_include_dirs(string):
        return [x[2:] for x in string.split() if x.startswith("-I")]

    def get_library_dirs(string):
        return [x[2:] for x in string.split() if x.startswith("-L")]

    def get_libraries(string):
        return [x[2:] for x in string.split() if x.startswith("-l")]

    # convert -Dfoo=bar to list of tuples [("foo", "bar")] expected by distutils
    def get_macros(string):
        def _macro(x):
            x = x[2:]    # drop "-D"
            if '=' in x:
                return tuple(x.split("=", 1))  # "-Dfoo=bar" => ("foo", "bar")
            else:
                return (x, None)               # "-Dfoo" => ("foo", None)
        return [_macro(x) for x in string.split() if x.startswith("-D")]

    def get_other_cflags(string):
        return [x for x in string.split() if not x.startswith("-I") and
                                             not x.startswith("-D")]

    def get_other_libs(string):
        return [x for x in string.split() if not x.startswith("-L") and
                                             not x.startswith("-l")]

    # return kwargs for given libname
    def kwargs(libname):
        fse = sys.getfilesystemencoding()
        all_cflags = call(libname, "--cflags")
        all_libs = call(libname, "--libs")
        return {
            "include_dirs": get_include_dirs(all_cflags),
            "library_dirs": get_library_dirs(all_libs),
            "libraries": get_libraries(all_libs),
            "define_macros": get_macros(all_cflags),
            "extra_compile_args": get_other_cflags(all_cflags),
            "extra_link_args": get_other_libs(all_libs),
            }

    # merge all arguments together
    ret = {}
    for libname in libs:
        lib_flags = kwargs(libname)
        merge_flags(ret, lib_flags)
    return ret

