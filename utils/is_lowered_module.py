
def is_lowered_module(obj: Any) -> bool:
    """
    This function is added to avoid using isinstance(obj,
    LoweredBackendModule) as it will import LoweredBackendModule, which may
    cause a circular import.
    """
    return type(obj).__name__ == LOWERED_BACKEND_MODULE_TYPE

