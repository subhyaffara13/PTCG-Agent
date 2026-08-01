
def find_spec(module, paths):
    finder = (
        importlib.machinery.PathFinder().find_spec
        if isinstance(paths, list)
        else importlib.util.find_spec
    )
    return finder(module, paths)


def find_spec(modpath: Iterable[str], path: Iterable[str] | None = None) -> ModuleSpec:
    """Find a spec for the given module.

    :type modpath: list or tuple
    :param modpath:
      split module's name (i.e name of a module or package split
      on '.'), with leading empty strings for explicit relative import

    :type path: list or None
    :param path:
      optional list of path where the module or package should be
      searched (use sys.path if nothing or None is given)

    :rtype: ModuleSpec
    :return: A module spec, which describes how the module was
             found and where.
    """
    return _find_spec(tuple(modpath), tuple(path) if path else None)

