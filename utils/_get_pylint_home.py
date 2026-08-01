
def _get_pylint_home() -> str:
    """Return the pylint home."""
    if "PYLINTHOME" in os.environ:
        return os.environ["PYLINTHOME"]
    return DEFAULT_PYLINT_HOME

