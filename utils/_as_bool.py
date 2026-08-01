
def _as_bool(value: str) -> bool:
    """Given a string value that represents True or False, returns the Boolean equivalent.
    Heavily inspired from distutils strtobool.
    """
    try:
        return _STR_BOOLEAN_MAPPING[value.lower()]
    except KeyError:
        raise ValueError(f"invalid truth value {value}")

