
def get_supported_modules() -> list[str]:
    """
    :returns: A list of all supported modules.
    """
    return [f for f in modules if check_module(f)]

