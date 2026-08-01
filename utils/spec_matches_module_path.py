
def spec_matches_module_path(module_spec: ModuleSpec | None, module_path: Path) -> bool:
    """Return true if the given ModuleSpec can be used to import the given module path."""
    if module_spec is None:
        return False

    if module_spec.origin:
        return Path(module_spec.origin) == module_path

    # Compare the path with the `module_spec.submodule_Search_Locations` in case
    # the module is part of a namespace package.
    # https://docs.python.org/3/library/importlib.html#importlib.machinery.ModuleSpec.submodule_search_locations
    if module_spec.submodule_search_locations:  # can be None.
        for path in module_spec.submodule_search_locations:
            if Path(path) == module_path:
                return True

    return False

