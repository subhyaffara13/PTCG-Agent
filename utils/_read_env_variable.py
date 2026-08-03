import os

def _read_env_variable(name: str) -> bool | str | None:
    value = os.environ.get(name)
    if value == "1":
        return True
    if value == "0":
        return False
    return value

