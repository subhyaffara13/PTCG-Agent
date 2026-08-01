
def deprecation(msg: str, *args: object):
    """Logs a deprecation warning to users."""
    warn(msg, *args, category=DeprecationWarning, stacklevel=2)


def deprecation(msg: str, *args: object):
    """Logs a deprecation warning to users."""
    warn(msg, *args, category=DeprecationWarning, stacklevel=2)


def deprecation(message: str, internal: str | list[str] = "jupyter_core/") -> None:
    """Generate a deprecation warning targeting the first frame that is not 'internal'

    internal is a string or list of strings, which if they appear in filenames in the
    frames, the frames will be considered internal. Changing this can be useful if, for example,
    we know that our internal code is calling out to another library.
    """
    _internal: list[str]
    _internal = [internal] if isinstance(internal, str) else internal

    # stack level of the first external frame from here
    stacklevel = _external_stacklevel(_internal)

    # The call to .warn adds one frame, so bump the stacklevel up by one
    warnings.warn(message, DeprecationWarning, stacklevel=stacklevel + 1)

