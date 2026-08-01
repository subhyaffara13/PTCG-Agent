
def is_opaque_type(cls: type[Any] | str) -> bool:
    """
    Checks if the given type is an opaque type.
    Also returns True for subclasses of registered opaque types.
    """
    if isinstance(cls, str):
        return torch._C._is_opaque_type_registered(cls)

    if not isinstance(cls, type):
        log.warning("Passed invalid type `%s` to is_opaque_type, returning False", cls)
        return False

    info = _resolve_opaque_type_info(cls)
    if info is None:
        return False

    return torch._C._is_opaque_type_registered(info.class_name)

