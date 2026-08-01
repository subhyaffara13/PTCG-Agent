
def registered_extensions() -> dict[str, str]:
    """
    Returns a dictionary containing all file extensions belonging
    to registered plugins
    """
    init()
    return EXTENSION

