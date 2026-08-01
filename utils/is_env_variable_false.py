
def is_env_variable_false(env_variable: str) -> bool:
    """Detect whether `env_variable` has been set to a false value in the environment"""
    return os.getenv(env_variable, "true").lower() in ("false", "0", "n", "no", "off")

