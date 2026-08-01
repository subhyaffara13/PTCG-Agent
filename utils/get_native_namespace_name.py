
def get_native_namespace_name(xp: ModuleType) -> str:
    """Return name for native namespace (without array_api_compat prefix)."""
    name = xp.__name__
    return name.removeprefix(f"{_compat_module_name()}.")

