
def load_module_from_file(filepath: str) -> types.ModuleType:
    """Load a Python module from it's path.

    :type filepath: str
    :param filepath: path to the python module or package

    :raise ImportError: if the module or package is not found

    :rtype: module
    :return: the loaded module
    """
    modpath = modpath_from_file(filepath)
    return load_module_from_modpath(modpath)

