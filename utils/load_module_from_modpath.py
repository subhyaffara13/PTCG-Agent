
def load_module_from_modpath(parts: Sequence[str]) -> types.ModuleType:
    """Load a python module from its split name.

    :param parts:
      python name of a module or package split on '.'

    :raise ImportError: if the module or package is not found

    :return: the loaded module
    """
    return load_module_from_name(".".join(parts))

