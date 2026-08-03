from typing import Any

def _lazy_import_utils_module(name: str) -> Any:
    """
    Handler for utils module lazy imports.

    This uses a custom implementation because utils module needs to use
    _get_utils_globals() instead of _get_litellm_globals() for caching.
    """
    # Check if this attribute exists in our map
    if name not in _UTILS_MODULE_IMPORT_MAP:
        raise AttributeError(f"Utils module lazy import: unknown attribute {name!r}")

    # Get the cache (where we store imported things) - use utils globals
    _globals = _get_utils_globals()

    # If we've already imported it, just return the cached version
    if name in _globals:
        return _globals[name]

    # Look up where to find this attribute
    module_path, attr_name = _UTILS_MODULE_IMPORT_MAP[name]

    # Import the module
    if module_path.startswith("."):
        module = importlib.import_module(module_path, package="litellm")
    else:
        module = importlib.import_module(module_path)

    # Get the actual attribute from the module
    value = getattr(module, attr_name)

    # Cache it so we don't have to import again next time
    _globals[name] = value

    # Return it
    return value

