
def modpath_from_file(filename: str, path: list[str] | None = None) -> list[str]:
    """Get the corresponding split module's name from a filename.

    This function will return the name of a module or package split on `.`.

    :type filename: str
    :param filename: file's path for which we want the module's name

    :type Optional[List[str]] path:
      Optional list of paths where the module or package should be
      searched, additionally to sys.path

    :raise ImportError:
      if the corresponding module's name has not been found

    :rtype: list(str)
    :return: the corresponding split module's name
    """
    return modpath_from_file_with_callback(filename, path, check_modpath_has_init)

