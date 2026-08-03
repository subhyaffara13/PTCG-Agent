import os

def envset(name: str, default: bool = False) -> bool: ...


def envset(name: str, default: None) -> bool | None: ...


def envset(name: str, default: bool | None = False) -> bool | None:
    """Return the boolean value of a given environment variable.

    An environment variable is considered set if it is assigned to a value
    other than 'no', 'n', 'false', 'off', '0', or '0.0' (case insensitive)

    If the environment variable is not defined, the default value is returned.
    """
    if name not in os.environ:
        return default

    return os.environ[name].lower() not in ["no", "n", "false", "off", "0", "0.0"]

