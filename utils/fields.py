
def fields(cls):
    """
    Return the tuple of *attrs* attributes for a class or instance.

    The tuple also allows accessing the fields by their names (see below for
    examples).

    Args:
        cls (type): Class or instance to introspect.

    Raises:
        TypeError: If *cls* is neither a class nor an *attrs* instance.

        attrs.exceptions.NotAnAttrsClassError:
            If *cls* is not an *attrs* class.

    Returns:
        tuple (with name accessors) of `attrs.Attribute`

    .. versionchanged:: 16.2.0 Returned tuple allows accessing the fields
       by name.
    .. versionchanged:: 23.1.0 Add support for generic classes.
    .. versionchanged:: 26.1.0 Add support for instances.
    """
    generic_base = get_generic_base(cls)

    if generic_base is None and not isinstance(cls, type):
        type_ = type(cls)
        if getattr(type_, "__attrs_attrs__", None) is None:
            msg = "Passed object must be a class or attrs instance."
            raise TypeError(msg)

        return fields(type_)

    attrs = getattr(cls, "__attrs_attrs__", None)

    if attrs is None:
        if generic_base is not None:
            attrs = getattr(generic_base, "__attrs_attrs__", None)
            if attrs is not None:
                # Even though this is global state, stick it on here to speed
                # it up. We rely on `cls` being cached for this to be
                # efficient.
                cls.__attrs_attrs__ = attrs
                return attrs
        msg = f"{cls!r} is not an attrs-decorated class."
        raise NotAnAttrsClassError(msg)

    return attrs

