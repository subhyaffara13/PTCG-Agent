
def is_opaque_value_type(cls: type[Any] | str) -> bool:
    """
    Checks if the given type is an opaque **value** type.
    See Note [Opaque Objects] for more information.
    """
    if not is_opaque_type(cls):
        return False

    if isinstance(cls, str):
        return _OPAQUE_TYPES_BY_NAME[cls].opaque_typ == "value"

    info = _resolve_opaque_type_info(cls)
    if info is None:
        return False
    return info.opaque_typ == "value"

