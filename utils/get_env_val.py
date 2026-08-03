import os

def get_env_val(env_str: str) -> str | None:
    return os.environ.get(env_str, None)

