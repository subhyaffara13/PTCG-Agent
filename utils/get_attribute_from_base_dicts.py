
def get_attribute_from_base_dicts(tp: type[Any], name: str) -> Any:
    """Get an attribute out of the `__dict__` following the MRO.
    This prevents the call to `__get__` on the descriptor, and allows
    us to get the original function for classmethod properties.

    Args:
        tp: The type or class to search for the attribute.
        name: The name of the attribute to retrieve.

    Returns:
        Any: The attribute value, if found.

    Raises:
        KeyError: If the attribute is not found in any class's `__dict__` in the MRO.
    """
    for base in reversed(mro(tp)):
        if name in base.__dict__:
            return base.__dict__[name]
    return tp.__dict__[name]  # raise the error

