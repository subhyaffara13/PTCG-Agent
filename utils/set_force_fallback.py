
def set_force_fallback(configval: str) -> None:
    """Set the config used to force LTC fallback"""
    torch._C._lazy._set_force_fallback(configval)

