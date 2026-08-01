
def _get_shared_cflags(do_link: bool) -> list[str]:
    if _IS_WINDOWS:
        """
        MSVC `/MD` using python `ucrtbase.dll` lib as runtime.
        https://learn.microsoft.com/en-us/cpp/c-runtime-library/crt-library-features?view=msvc-170
        """
        return ["DLL", "MD"]
    if platform.system() == "Darwin" and "clang" in get_cpp_compiler():
        # This causes undefined symbols to behave the same as linux
        return ["shared", "fPIC", "undefined dynamic_lookup"]
    flags = []
    if do_link:
        flags.append("shared")

    flags.append("fPIC")
    return flags

