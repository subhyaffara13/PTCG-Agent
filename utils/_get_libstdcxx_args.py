
def _get_libstdcxx_args() -> tuple[list[str], list[str]]:
    """
    For fbcode cpu case, we should link stdc++ instead assuming the binary where dlopen is executed is built with dynamic stdc++.
    """
    lib_dir_paths: list[str] = []
    libs: list[str] = []
    if config.is_fbcode():
        lib_dir_paths = [sysconfig.get_config_var("LIBDIR")]
        libs.append("stdc++")

    return lib_dir_paths, libs

