from typing import Any

def _generic_lazy_import(
    name: str, import_map: dict[str, tuple[str, str]], category: str
) -> Any:
    """
    Generic function that handles lazy importing for most attributes.

    This is the workhorse function - it does the actual importing and caching.
    Most handler functions just call this with their specific import map.

    Steps:
    1. Check if the name exists in the import map (if not, raise error)
    2. Check if we've already imported it (if yes, return cached value)
    3. Look up where to find it (module_path and attr_name from the map)
    4. Import the module (Python caches this automatically)
    5. Get the attribute from the module
    6. Cache it in _globals so we don't import again
    7. Return it

    Args:
        name: The attribute name someone is trying to access (e.g., "ModelResponse")
        import_map: Dictionary telling us where to find each attribute
                   Format: {"ModelResponse": (".utils", "ModelResponse")}
        category: Just for error messages (e.g., "Utils", "Cost calculator")
    """
    # Step 1: Make sure this attribute exists in our map
    if name not in import_map:
        raise AttributeError(f"{category} lazy import: unknown attribute {name!r}")

    # Step 2: Get the cache (where we store imported things)
    _globals = _get_litellm_globals()

    # Step 3: If we've already imported it, just return the cached version
    if name in _globals:
        return _globals[name]

    # Step 4: Look up where to find this attribute
    # The map tells us: (module_path, attribute_name)
    # Example: (".utils", "ModelResponse") means "look in .utils module, get ModelResponse"
    module_path, attr_name = import_map[name]

    # Step 5: Import the module
    # Python automatically caches modules in sys.modules, so calling this twice is fast
    # If module_path starts with ".", it's a relative import (needs package="litellm")
    # Otherwise it's an absolute import (like "litellm.caching.caching")
    if module_path.startswith("."):
        module = importlib.import_module(module_path, package="litellm")
    else:
        module = importlib.import_module(module_path)

    # Step 6: Get the actual attribute from the module
    # Example: getattr(utils_module, "ModelResponse") returns the ModelResponse class
    value = getattr(module, attr_name)

    # Step 7: Cache it so we don't have to import again next time
    _globals[name] = value

    # Step 8: Return it
    return value

