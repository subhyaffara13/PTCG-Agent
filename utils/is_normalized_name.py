
def is_normalized_name(name: str) -> bool:
    """
    Check if a name is already normalized (i.e. :func:`canonicalize_name` would
    roundtrip to the same value).

    :param str name: The name to check.

    >>> from packaging.utils import is_normalized_name
    >>> is_normalized_name("requests")
    True
    >>> is_normalized_name("Django")
    False
    """
    return _normalized_regex.fullmatch(name) is not None


def is_normalized_name(name: str) -> bool:
    return _normalized_regex.fullmatch(name) is not None


def is_normalized_name(name: str) -> bool:
    """
    Check if a name is already normalized (i.e. :func:`canonicalize_name` would
    roundtrip to the same value).

    :param str name: The name to check.

    >>> from packaging.utils import is_normalized_name
    >>> is_normalized_name("requests")
    True
    >>> is_normalized_name("Django")
    False
    """
    return _normalized_regex.fullmatch(name) is not None

