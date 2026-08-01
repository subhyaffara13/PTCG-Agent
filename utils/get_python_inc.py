
def get_python_inc(plat_specific: bool = False, prefix: str | None = None) -> str:
    """Return the directory containing installed Python header files.

    If 'plat_specific' is false (the default), this is the path to the
    non-platform-specific header files, i.e. Python.h and so on;
    otherwise, this is the path to platform-specific header files
    (namely pyconfig.h).

    If 'prefix' is supplied, use it instead of sys.base_prefix or
    sys.base_exec_prefix -- i.e., ignore 'plat_specific'.
    """
    default_prefix = BASE_EXEC_PREFIX if plat_specific else BASE_PREFIX
    resolved_prefix = prefix if prefix is not None else default_prefix
    # MinGW imitates posix like layout, but os.name != posix
    os_name = "posix" if is_mingw() else os.name
    try:
        getter = globals()[f'_get_python_inc_{os_name}']
    except KeyError:
        raise DistutilsPlatformError(
            "I don't know where Python installs its C header files "
            f"on platform '{os.name}'"
        )
    return getter(resolved_prefix, prefix, plat_specific)

