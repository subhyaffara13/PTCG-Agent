from typing import Optional

def get_opik_config_variable(
    key: str, user_value: Optional[str] = None, default_value: Optional[str] = None
) -> Optional[str]:
    """
    Get the configuration value of a variable, order priority is:
    1. user provided value
    2. environment variable
    3. Opik configuration file
    4. default value
    """
    # Return user provided value if it is not None
    if user_value is not None:
        return user_value

    # Return environment variable if it is not None
    env_value = _get_env_variable(key)
    if env_value is not None:
        return env_value

    # Return value from Opik configuration file if it is not None
    config_values = _read_opik_config_file()

    if key in config_values:
        return config_values[key]

    # Return default value if it is not None
    return default_value

