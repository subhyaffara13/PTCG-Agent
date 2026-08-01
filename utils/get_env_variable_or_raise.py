
def get_env_variable_or_raise(env_name: str) -> str:
    r"""
    Tries to retrieve environment variable. Raises ``ValueError``
    if no environment variable found.

    Args:
        env_name (str): Name of the env variable
    """
    value = os.environ.get(env_name, None)
    if value is None:
        msg = f"Environment variable {env_name} expected, but not set"
        raise ValueError(msg)
    return value

