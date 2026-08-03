import sys

def find_module_path_and_all_py3(
    inspect: ModuleInspect, module: str, verbose: bool
) -> tuple[str | None, list[str] | None] | None:
    """Find module and determine __all__ for a Python 3 module.

    Return None if the module is a C or pyc-only module.
    Return (module_path, __all__) if it is a Python module.
    Raise CantImport if import failed.
    """
    if module in NOT_IMPORTABLE_MODULES:
        raise CantImport(module, "")

    # TODO: Support custom interpreters.
    if verbose:
        print(f"Trying to import {module!r} for runtime introspection")
    try:
        mod = inspect.get_package_properties(module)
    except InspectError as e:
        # Fall back to finding the module using sys.path.
        path = find_module_path_using_sys_path(module, sys.path)
        if path is None:
            raise CantImport(module, str(e)) from e
        return path, None
    if mod.is_c_module:
        return None
    return mod.file, mod.all

