import os

def is_env_variable_true(env_variable: str) -> bool:
    """Detect whether `env_variable` has been set to a true value in the environment"""
    return os.getenv(env_variable, "false").lower() in ("true", "1", "y", "yes", "on")

