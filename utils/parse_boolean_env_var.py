
def parse_boolean_env_var(env_var_value: str | None, default: bool) -> bool:
    if env_var_value is None:
        return default
    value = env_var_value.lower()
    if value in ("y", "yes", "t", "true", "on", "1"):
        return True
    if value in ("n", "no", "f", "false", "off", "0"):
        return False
    return default

