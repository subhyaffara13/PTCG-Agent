import sys

def walk_packages(
    inspect: ModuleInspect, packages: list[str], verbose: bool = False
) -> Iterator[str]:
    """Iterates through all packages and sub-packages in the given list.

    This uses runtime imports (in another process) to find both Python and C modules.
    For Python packages we simply pass the __path__ attribute to pkgutil.walk_packages() to
    get the content of the package (all subpackages and modules).  However, packages in C
    extensions do not have this attribute, so we have to roll out our own logic: recursively
    find all modules imported in the package that have matching names.
    """
    for package_name in packages:
        if package_name in NOT_IMPORTABLE_MODULES:
            print(f"{package_name}: Skipped (blacklisted)")
            continue
        if verbose:
            print(f"Trying to import {package_name!r} for runtime introspection")
        try:
            prop = inspect.get_package_properties(package_name)
        except InspectError:
            if verbose:
                tb = traceback.format_exc()
                sys.stderr.write(tb)
            report_missing(package_name)
            continue
        yield prop.name
        if prop.is_c_module:
            # Recursively iterate through the subpackages
            yield from walk_packages(inspect, prop.subpackages, verbose)
        else:
            yield from prop.subpackages

