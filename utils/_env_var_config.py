
def _env_var_config(env_var: str, default: bool) -> bool:
    env_val = _env_var_val(env_var, None)
    if env_val is not None:
        return env_val == "1"
    return default

