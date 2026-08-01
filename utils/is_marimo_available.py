
def is_marimo_available(min_version=MARIMO_MIN_VERSION, max_version=None):
    """Is Marimo available?"""
    try:
        raise_if_marimo_is_not_available(min_version=min_version, max_version=max_version)
        return True
    except MarimoError:
        return False

