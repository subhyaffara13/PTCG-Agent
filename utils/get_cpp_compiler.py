import os
import sys

def get_cpp_compiler() -> str:
    if (
        config.aot_inductor.cross_target_platform == "windows"
        and sys.platform != "win32"
    ):
        # we're doing cross-compilation
        compiler = MINGW_GXX
        if not config.aot_inductor.package_cpp_only:
            check_mingw_win32_flavor(compiler)
        return compiler

    if _IS_WINDOWS:
        compiler = os.environ.get("CXX", "cl")
        compiler = normalize_path_separator(compiler)
        check_compiler_exist_windows(compiler)
        check_msvc_cl_language_id(compiler)
    else:
        if config.is_fbcode():
            return build_paths.cc
        if isinstance(config.cpp.cxx, (list, tuple)):
            search = tuple(config.cpp.cxx)
        else:
            search = (config.cpp.cxx,)
        compiler = cpp_compiler_search(search)
    return compiler

