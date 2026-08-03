import os

def should_force_color() -> bool:
    env_var = os.getenv("MYPY_FORCE_COLOR", os.getenv("FORCE_COLOR", "0"))
    try:
        return bool(int(env_var))
    except ValueError:
        return bool(env_var)

