
def _get_attr_type(type_: type) -> ir.AttributeType:
    """Obtain the type of the attribute from a Python class."""
    try:
        if type_ in _PY_TYPE_TO_ATTR_TYPE:
            return _PY_TYPE_TO_ATTR_TYPE[type_]
        origin_type = typing.get_origin(type_)
        if origin_type is None:
            return ir.AttributeType.UNDEFINED
        if origin_type in (
            collections.abc.Sequence,
            Sequence,
            list,
            list,
            tuple,
            tuple,
        ):
            inner_type = typing.get_args(type_)[0]
            if inner_type in _LIST_TYPE_TO_ATTR_TYPE:
                return _LIST_TYPE_TO_ATTR_TYPE[inner_type]
    except TypeError:
        logger.warning("TypeError when checking %s.", type_, exc_info=True)
    return ir.AttributeType.UNDEFINED

