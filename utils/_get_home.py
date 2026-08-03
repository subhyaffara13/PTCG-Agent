import os

def _get_home() -> str:
    return os.getenv(HOME_PATH_ENV_VAR, DEFAULT_HOME_PATH)

