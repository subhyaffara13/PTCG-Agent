import os

def search_pypath(
    module_name: str, *, consider_namespace_packages: bool = False
) -> str | None:
    """Search sys.path for the given a dotted module name, and return its file
    system path if found."""
    try:
        spec = importlib.util.find_spec(module_name)
    # AttributeError: looks like package module, but actually filename
    # ImportError: module does not exist
    # ValueError: not a module name
    except (AttributeError, ImportError, ValueError):
        return None

    if spec is None:
        return None

    if (
        spec.submodule_search_locations is None
        or len(spec.submodule_search_locations) == 0
    ):
        # Must be a simple module.
        return spec.origin

    if consider_namespace_packages:
        # If submodule_search_locations is set, it's a package (regular or namespace).
        # Typically there is a single entry, but documentation claims it can be empty too
        #  (e.g. if the package has no physical location).
        return spec.submodule_search_locations[0]

    if spec.origin is None:
        # This is only the case for namespace packages
        return None

    return os.path.dirname(spec.origin)

