
def is_standard_module(modname: str, std_path: Iterable[str] | None = None) -> bool:
    """Try to guess if a module is a standard python module (by default,
    see `std_path` parameter's description).

    :param modname: name of the module we are interested in

    :param std_path: list of path considered has standard

    :return:
      true if the module:
      - is located on the path listed in one of the directory in `std_path`
      - is a built-in module
    """
    warnings.warn(
        "is_standard_module() is deprecated. Use, is_stdlib_module() or module_in_path() instead",
        DeprecationWarning,
        stacklevel=2,
    )

    modname = modname.split(".")[0]
    try:
        filename = file_from_modpath([modname])
    except ImportError:
        # import failed, i'm probably not so wrong by supposing it's
        # not standard...
        return False
    # modules which are not living in a file are considered standard
    # (sys and __builtin__ for instance)
    if filename is None:
        # we assume there are no namespaces in stdlib
        return not util.is_namespace(modname)
    filename = _normalize_path(filename)
    for path in EXT_LIB_DIRS:
        if filename.startswith(_cache_normalize_path(path)):
            return False
    if std_path is None:
        std_path = STD_LIB_DIRS

    return any(filename.startswith(_cache_normalize_path(path)) for path in std_path)

