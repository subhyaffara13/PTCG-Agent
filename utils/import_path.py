
def import_path(
    path: str | os.PathLike[str],
    *,
    mode: str | ImportMode = ImportMode.prepend,
    root: Path,
    consider_namespace_packages: bool,
) -> ModuleType:
    """
    Import and return a module from the given path, which can be a file (a module) or
    a directory (a package).

    :param path:
        Path to the file to import.

    :param mode:
        Controls the underlying import mechanism that will be used:

        * ImportMode.prepend: the directory containing the module (or package, taking
          `__init__.py` files into account) will be put at the *start* of `sys.path` before
          being imported with `importlib.import_module`.

        * ImportMode.append: same as `prepend`, but the directory will be appended
          to the end of `sys.path`, if not already in `sys.path`.

        * ImportMode.importlib: uses more fine control mechanisms provided by `importlib`
          to import the module, which avoids having to muck with `sys.path` at all. It effectively
          allows having same-named test modules in different places.

    :param root:
        Used as an anchor when mode == ImportMode.importlib to obtain
        a unique name for the module being imported so it can safely be stored
        into ``sys.modules``.

    :param consider_namespace_packages:
        If True, consider namespace packages when resolving module names.

    :raises ImportPathMismatchError:
        If after importing the given `path` and the module `__file__`
        are different. Only raised in `prepend` and `append` modes.
    """
    path = Path(path)
    mode = ImportMode(mode)

    if not path.exists():
        raise ImportError(path)

    if mode is ImportMode.importlib:
        # Try to import this module using the standard import mechanisms, but
        # without touching sys.path.
        try:
            _, module_name = resolve_pkg_root_and_module_name(
                path, consider_namespace_packages=consider_namespace_packages
            )
        except CouldNotResolvePathError:
            pass
        else:
            # If the given module name is already in sys.modules, do not import it again.
            with contextlib.suppress(KeyError):
                return sys.modules[module_name]

            mod = _import_module_using_spec(module_name, path, insert_modules=False)
            if mod is not None:
                return mod

        # Could not import the module with the current sys.path, so we fall back
        # to importing the file as a single module, not being a part of a package.
        module_name = module_name_from_path(path, root)
        with contextlib.suppress(KeyError):
            return sys.modules[module_name]

        mod = _import_module_using_spec(module_name, path, insert_modules=True)
        if mod is None:
            raise ImportError(f"Can't find module {module_name} at location {path}")
        return mod

    try:
        pkg_root, module_name = resolve_pkg_root_and_module_name(
            path, consider_namespace_packages=consider_namespace_packages
        )
    except CouldNotResolvePathError:
        pkg_root, module_name = path.parent, path.stem

    # Change sys.path permanently: restoring it at the end of this function would cause surprising
    # problems because of delayed imports: for example, a conftest.py file imported by this function
    # might have local imports, which would fail at runtime if we restored sys.path.
    if mode is ImportMode.append:
        if str(pkg_root) not in sys.path:
            sys.path.append(str(pkg_root))
    elif mode is ImportMode.prepend:
        if str(pkg_root) != sys.path[0]:
            sys.path.insert(0, str(pkg_root))
    else:
        assert_never(mode)

    importlib.import_module(module_name)

    mod = sys.modules[module_name]
    if path.name == "__init__.py":
        return mod

    ignore = os.environ.get("PY_IGNORE_IMPORTMISMATCH", "")
    if ignore != "1":
        module_file = mod.__file__
        if module_file is None:
            raise ImportPathMismatchError(module_name, module_file, path)

        if module_file.endswith((".pyc", ".pyo")):
            module_file = module_file[:-1]
        if module_file.endswith(os.sep + "__init__.py"):
            module_file = module_file[: -(len(os.sep + "__init__.py"))]

        try:
            is_same = _is_same(str(path), module_file)
        except FileNotFoundError:
            is_same = False

        if not is_same:
            raise ImportPathMismatchError(module_name, module_file, path)

    return mod

