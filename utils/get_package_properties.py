
def get_package_properties(package_id: str) -> ModuleProperties:
    """Use runtime introspection to get information about a module/package."""
    try:
        package = importlib.import_module(package_id)
    except BaseException as e:
        raise InspectError(str(e)) from e
    name = getattr(package, "__name__", package_id)
    file = getattr(package, "__file__", None)
    path: list[str] | None = getattr(package, "__path__", None)
    if not isinstance(path, list):
        path = None
    pkg_all = getattr(package, "__all__", None)
    if pkg_all is not None:
        try:
            pkg_all = list(pkg_all)
        except Exception:
            pkg_all = None
    is_c = is_c_module(package)

    if path is None:
        # Object has no path; this means it's either a module inside a package
        # (and thus no sub-packages), or it could be a C extension package.
        if is_c:
            # This is a C extension module, now get the list of all sub-packages
            # using the inspect module
            subpackages = [
                package.__name__ + "." + name
                for name, val in inspect.getmembers(package)
                if inspect.ismodule(val) and val.__name__ == package.__name__ + "." + name
            ]
        else:
            # It's a module inside a package.  There's nothing else to walk/yield.
            subpackages = []
    else:
        all_packages = pkgutil.walk_packages(
            path, prefix=package.__name__ + ".", onerror=lambda r: None
        )
        subpackages = [qualified_name for importer, qualified_name, ispkg in all_packages]
    return ModuleProperties(
        name=name, file=file, path=path, all=pkg_all, is_c_module=is_c, subpackages=subpackages
    )

