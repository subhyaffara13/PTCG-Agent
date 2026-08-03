import os

def get_config_path():
    """Returns the absolute path the the Cloud SDK's configuration directory.

    Returns:
        str: The Cloud SDK config path.
    """
    # If the path is explicitly set, return that.
    try:
        return os.environ[environment_vars.CLOUD_SDK_CONFIG_DIR]
    except KeyError:
        pass

    # Non-windows systems store this at ~/.config/gcloud
    if os.name != "nt":
        return os.path.join(os.path.expanduser("~"), ".config", _CONFIG_DIRECTORY)
    # Windows systems store config at %APPDATA%\gcloud
    else:
        try:
            return os.path.join(
                os.environ[_WINDOWS_CONFIG_ROOT_ENV_VAR], _CONFIG_DIRECTORY
            )
        except KeyError:
            # This should never happen unless someone is really
            # messing with things, but we'll cover the case anyway.
            drive = os.environ.get("SystemDrive", "C:")
            return os.path.join(drive, "\\", _CONFIG_DIRECTORY)

