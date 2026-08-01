
def ensure_valid(ep):
    """
    Exercise one of the dynamic properties to trigger
    the pattern match.

    This function is deprecated in favor of importlib_metadata 8.7 and
    Python 3.14 importlib.metadata, which validates entry points on
    construction.
    """
    try:
        ep.extras
    except (AttributeError, AssertionError) as ex:
        # Why both? See https://github.com/python/importlib_metadata/issues/488
        msg = (
            f"Problems to parse {ep}.\nPlease ensure entry-point follows the spec: "
            "https://packaging.python.org/en/latest/specifications/entry-points/"
        )
        raise OptionError(msg) from ex

