import sys
from pathlib import Path


def _import_module_using_spec(
    module_name: str, module_path: Path, *, insert_modules: bool
) -> ModuleType | None:
    """
    Tries to import a module by its canonical name, path, and its parent location.

    :param module_name:
        The expected module name, will become the key of `sys.modules`.

    :param module_path:
        The file path of the module, for example `/foo/bar/test_demo.py`.
        If module is a package, pass the path to the  `__init__.py` of the package.
        If module is a namespace package, pass directory path.

    :param insert_modules:
        If True, will call `insert_missing_modules` to create empty intermediate modules
        with made-up module names (when importing test files not reachable from `sys.path`).

    Example 1 of parent_module_*:

        module_name:        "a.b.c.demo"
        module_path:        Path("a/b/c/demo.py")
        if "a.b.c" is package ("a/b/c/__init__.py" exists), then
            parent_module_name:         "a.b.c"
            parent_module_path:         Path("a/b/c/__init__.py")
        else:
            parent_module_name:         "a.b.c"
            parent_module_path:         Path("a/b/c")

    Example 2 of parent_module_*:

        module_name:        "a.b.c"
        module_path:        Path("a/b/c/__init__.py")
        if  "a.b" is package ("a/b/__init__.py" exists), then
            parent_module_name:         "a.b"
            parent_module_path:         Path("a/b/__init__.py")
        else:
            parent_module_name:         "a.b"
            parent_module_path:         Path("a/b/")
    """
    # Attempt to import the parent module, seems is our responsibility:
    # https://github.com/python/cpython/blob/73906d5c908c1e0b73c5436faeff7d93698fc074/Lib/importlib/_bootstrap.py#L1308-L1311
    parent_module_name, _, name = module_name.rpartition(".")
    parent_module: ModuleType | None = None
    if parent_module_name:
        parent_module = sys.modules.get(parent_module_name)
        # If the parent_module lacks the `__path__` attribute, AttributeError when finding a submodule's spec,
        # requiring re-import according to the path.
        need_reimport = not hasattr(parent_module, "__path__")
        if parent_module is None or need_reimport:
            # Get parent_location based on location, get parent_path based on path.
            if module_path.name == "__init__.py":
                # If the current module is in a package,
                # need to leave the package first and then enter the parent module.
                parent_module_path = module_path.parent.parent
            else:
                parent_module_path = module_path.parent

            if (parent_module_path / "__init__.py").is_file():
                # If the parent module is a package, loading by  __init__.py file.
                parent_module_path = parent_module_path / "__init__.py"

            parent_module = _import_module_using_spec(
                parent_module_name,
                parent_module_path,
                insert_modules=insert_modules,
            )

    # Checking with sys.meta_path first in case one of its hooks can import this module,
    # such as our own assertion-rewrite hook.
    find_spec_path = [str(module_path.parent)]
    for meta_importer in sys.meta_path:
        spec = meta_importer.find_spec(module_name, find_spec_path)

        if spec_matches_module_path(spec, module_path):
            break
    else:
        loader = None
        if module_path.is_dir():
            # The `spec_from_file_location` matches a loader based on the file extension by default.
            # For a namespace package, need to manually specify a loader.
            loader = NamespaceLoader(name, module_path, PathFinder())  # type: ignore[arg-type]

        spec = importlib.util.spec_from_file_location(
            module_name, str(module_path), loader=loader
        )

    if spec_matches_module_path(spec, module_path):
        assert spec is not None
        # Find spec and import this module.
        mod = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = mod
        spec.loader.exec_module(mod)  # type: ignore[union-attr]

        # Set this module as an attribute of the parent module (#12194).
        if parent_module is not None:
            setattr(parent_module, name, mod)

        if insert_modules:
            insert_missing_modules(sys.modules, module_name)
        return mod

    return None

