
def check_extras(dist, attr, value):
    """Verify that extras_require mapping is valid"""
    try:
        list(itertools.starmap(_check_extra, value.items()))
    except (TypeError, ValueError, AttributeError) as e:
        raise DistutilsSetupError(
            "'extras_require' must be a dictionary whose values are "
            "strings or lists of strings containing valid project/version "
            "requirement specifiers."
        ) from e

