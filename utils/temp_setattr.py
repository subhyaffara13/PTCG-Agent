
def temp_setattr(obj, attr: str, value, condition: bool = True) -> Generator[None]:
    """
    Temporarily set attribute on an object.

    Parameters
    ----------
    obj : object
        Object whose attribute will be modified.
    attr : str
        Attribute to modify.
    value : Any
        Value to temporarily set attribute to.
    condition : bool, default True
        Whether to set the attribute. Provided in order to not have to
        conditionally use this context manager.

    Yields
    ------
    object : obj with modified attribute.
    """
    if condition:
        old_value = getattr(obj, attr)
        setattr(obj, attr, value)
    try:
        yield obj
    finally:
        if condition:
            setattr(obj, attr, old_value)

