
def _should_use_importlib_metadata() -> bool:
    """Whether to use the ``importlib.metadata`` or ``pkg_resources`` backend.

    By default, pip uses ``importlib.metadata`` on Python 3.11+, and
    ``pkg_resources`` otherwise. Up to Python 3.13, This can be
    overridden by a couple of ways:

    * If environment variable ``_PIP_USE_IMPORTLIB_METADATA`` is set, it
      dictates whether ``importlib.metadata`` is used, for Python <3.14.
    * On Python 3.11, 3.12 and 3.13, Python distributors can patch
      ``importlib.metadata`` to add a global constant
      ``_PIP_USE_IMPORTLIB_METADATA = False``. This makes pip use
      ``pkg_resources`` (unless the user set the aforementioned environment
      variable to *True*).

    On Python 3.14+, the ``pkg_resources`` backend cannot be used.
    """
    if sys.version_info >= (3, 14):
        # On Python >=3.14 we only support importlib.metadata.
        return True
    with contextlib.suppress(KeyError, ValueError):
        # On Python <3.14, if the environment variable is set, we obey what it says.
        return bool(strtobool(os.environ["_PIP_USE_IMPORTLIB_METADATA"]))
    if sys.version_info < (3, 11):
        # On Python <3.11, we always use pkg_resources, unless the environment
        # variable was set.
        return False
    # On Python 3.11, 3.12 and 3.13, we check if the global constant is set.
    import importlib.metadata

    return bool(getattr(importlib.metadata, "_PIP_USE_IMPORTLIB_METADATA", True))

