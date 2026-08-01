
def use_platform_dirs() -> bool:
    """Determine if platformdirs should be used for system-specific paths.

    The default is False.
    """
    return envset("JUPYTER_PLATFORM_DIRS", False)

