
def get_force_fallback() -> str:
    """Get the config used to force LTC fallback"""
    return torch._C._lazy._get_force_fallback()

