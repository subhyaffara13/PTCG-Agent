import os

def _env_var_val(env_var: str, default: T) -> str | T:
    """Get the value of an environment variable or return the default.

    Args:
        env_var: Environment variable name to check
        default: Default value to return if environment variable is not set

    Returns:
        The value from the environment variable as a string, or the default if not set
    """
    return os.environ.get(env_var, default)

