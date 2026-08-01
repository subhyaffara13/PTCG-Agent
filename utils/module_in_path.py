
def module_in_path(modname: str, path: str | Iterable[str]) -> bool:
    """Try to determine if a module is imported from one of the specified paths

    :param modname: name of the module

    :param path: paths to consider

    :return:
      true if the module:
      - is located on the path listed in one of the directory in `paths`
    """

    modname = modname.split(".")[0]
    try:
        filename = file_from_modpath([modname])
    except ImportError:
        # Import failed, we can't check path if we don't know it
        return False

    if filename is None:
        # No filename likely means it's compiled in, or potentially a namespace
        return False
    filename = _normalize_path(filename)

    if isinstance(path, str):
        return filename.startswith(_cache_normalize_path(path))

    return any(filename.startswith(_cache_normalize_path(entry)) for entry in path)

