import pathlib

def get_pandas_objects(
    module_name: str, recurse: bool
) -> list[tuple[str, str, object]]:
    """
    Get all pandas objects within a module.

    An object is determined to be part of pandas if it has a string
    __module__ attribute that starts with ``"pandas"``.

    Parameters
    ----------
    module_name : str
        Name of the module to search.
    recurse : bool
        Whether to search submodules.

    Returns
    -------
        List of all objects that are determined to be a part of pandas.
    """
    module = importlib.import_module(module_name)
    objs = []

    for name, obj in inspect.getmembers(module):
        module_dunder = getattr(obj, "__module__", None)
        if isinstance(module_dunder, str) and module_dunder.startswith("pandas"):
            objs.append((module_name, name, obj))

    if not recurse:
        return objs

    # __file__ can, but shouldn't, be None
    assert isinstance(module.__file__, str)
    paths = [pathlib.Path(module.__file__).parent]
    for module_info in pkgutil.walk_packages(paths):
        name = module_info.name
        if name.startswith("_") or name == "internals":
            continue
        objs.extend(
            get_pandas_objects(f"{module.__name__}.{name}", recurse=module_info.ispkg)
        )
    return objs

