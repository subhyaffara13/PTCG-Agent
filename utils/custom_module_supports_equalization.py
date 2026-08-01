
def custom_module_supports_equalization(module) -> bool:
    """Checks if the custom node supports equalization."""
    return type(module) in CUSTOM_MODULE_SUPP_LIST

