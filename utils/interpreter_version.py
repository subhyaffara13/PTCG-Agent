import sys

def interpreter_version(*, warn: bool = False) -> str:
    """
    Returns the running interpreter's version.

    This typically acts as the suffix to the :attr:`~Tag.interpreter` tag.

    :param bool warn: Whether warnings should be logged. Defaults to ``False``.
    """
    version = _get_config_var("py_version_nodot", warn=warn)
    return str(version) if version else _version_nodot(sys.version_info[:2])


def interpreter_version(*, warn: bool = False) -> str:
    """
    Returns the version of the running interpreter.
    """
    version = _get_config_var("py_version_nodot", warn=warn)
    return str(version) if version else _version_nodot(sys.version_info[:2])


def interpreter_version(*, warn: bool = False) -> str:
    """
    Returns the version of the running interpreter.
    """
    version = _get_config_var("py_version_nodot", warn=warn)
    if version:
        version = str(version)
    else:
        version = _version_nodot(sys.version_info[:2])
    return version


def interpreter_version(*, warn: bool = False) -> str:
    """
    Returns the running interpreter's version.

    This typically acts as the suffix to the :attr:`~Tag.interpreter` tag.

    :param bool warn: Whether warnings should be logged. Defaults to ``False``.
    """
    version = _get_config_var("py_version_nodot", warn=warn)
    return str(version) if version else _version_nodot(sys.version_info[:2])

