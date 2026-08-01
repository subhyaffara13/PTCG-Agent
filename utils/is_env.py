
def is_env(env_name: str) -> bool:
    return bool(re.fullmatch("[a-zA-Z_]+_v[0-9]+", env_name))

