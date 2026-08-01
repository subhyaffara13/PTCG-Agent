
def canonicalize_name(name: str, *, validate: bool = False) -> NormalizedName:
    """
    This function takes a valid Python package or extra name, and returns the
    normalized form of it.

    The return type is typed as :class:`NormalizedName`. This allows type
    checkers to help require that a string has passed through this function
    before use.

    If **validate** is true, then the function will check if **name** is a valid
    distribution name before normalizing.

    :param str name: The name to normalize.
    :param bool validate: Check whether the name is a valid distribution name.
    :raises InvalidName: If **validate** is true and the name is not an
        acceptable distribution name.

    >>> from packaging.utils import canonicalize_name
    >>> canonicalize_name("Django")
    'django'
    >>> canonicalize_name("oslo.concurrency")
    'oslo-concurrency'
    >>> canonicalize_name("requests")
    'requests'
    """
    if validate and not _validate_regex.fullmatch(name):
        raise InvalidName(f"name is invalid: {name!r}")
    # Ensure all ``.`` and ``_`` are ``-``
    # Emulates ``re.sub(r"[-_.]+", "-", name).lower()`` from PEP 503
    # Much faster than re, and even faster than str.translate
    value = name.lower().replace("_", "-").replace(".", "-")
    # Condense repeats (faster than regex)
    while "--" in value:
        value = value.replace("--", "-")
    return cast("NormalizedName", value)


def canonicalize_name(name: str, *, validate: bool = False) -> NormalizedName:
    if validate and not _validate_regex.fullmatch(name):
        raise InvalidName(f"name is invalid: {name!r}")
    # Ensure all ``.`` and ``_`` are ``-``
    # Emulates ``re.sub(r"[-_.]+", "-", name).lower()`` from PEP 503
    # Much faster than re, and even faster than str.translate
    value = name.lower().replace("_", "-").replace(".", "-")
    # Condense repeats (faster than regex)
    while "--" in value:
        value = value.replace("--", "-")
    return cast("NormalizedName", value)


def canonicalize_name(name: str) -> NormalizedName:
    # This is taken from PEP 503.
    value = _canonicalize_regex.sub("-", name).lower()
    return cast(NormalizedName, value)


def canonicalize_name(name: str, *, validate: bool = False) -> NormalizedName:
    """
    This function takes a valid Python package or extra name, and returns the
    normalized form of it.

    The return type is typed as :class:`NormalizedName`. This allows type
    checkers to help require that a string has passed through this function
    before use.

    If **validate** is true, then the function will check if **name** is a valid
    distribution name before normalizing.

    :param str name: The name to normalize.
    :param bool validate: Check whether the name is a valid distribution name.
    :raises InvalidName: If **validate** is true and the name is not an
        acceptable distribution name.

    >>> from packaging.utils import canonicalize_name
    >>> canonicalize_name("Django")
    'django'
    >>> canonicalize_name("oslo.concurrency")
    'oslo-concurrency'
    >>> canonicalize_name("requests")
    'requests'
    """
    if validate and not _validate_regex.fullmatch(name):
        raise InvalidName(f"name is invalid: {name!r}")
    # Ensure all ``.`` and ``_`` are ``-``
    # Emulates ``re.sub(r"[-_.]+", "-", name).lower()`` from PEP 503
    # Much faster than re, and even faster than str.translate
    value = name.lower().replace("_", "-").replace(".", "-")
    # Condense repeats (faster than regex)
    while "--" in value:
        value = value.replace("--", "-")
    return cast("NormalizedName", value)

