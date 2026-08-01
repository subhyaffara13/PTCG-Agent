
def _check_config_path(config_path):
    """Checks for config file path. If it exists, returns the absolute path with user expansion;
    otherwise returns None.

    Args:
        config_path (str): The config file path for either context_aware_metadata.json or certificate_config.json for example

    Returns:
        str: absolute path if exists and None otherwise.
    """
    config_path = path.expanduser(config_path)
    if not path.exists(config_path):
        _LOGGER.debug("%s is not found.", config_path)
        return None
    return config_path

