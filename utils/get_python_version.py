import sys

def get_python_version() -> str:
    """Find and format the python implementation and version.

    :returns:
        Implementation name, version, and platform as a string.
    """
    return "{} {} on {}".format(
        platform.python_implementation(),
        platform.python_version(),
        platform.system(),
    )


def get_python_version() -> str:
    try:
        return platform.python_version()
    except Exception:
        return "unknown"


def get_python_version():
    """Return a string containing the major and minor Python version,
    leaving off the patchlevel.  Sample return values could be '1.5'
    or '2.2'.
    """
    return f'{sys.version_info.major}.{sys.version_info.minor}'


def get_python_version() -> str:
    return _PY_VERSION

