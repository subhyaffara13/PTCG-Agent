
def supported_self_type(
    typ: ProperType, allow_callable: bool = True, allow_instances: bool = True
) -> bool:
    """Is this a supported kind of explicit self-types?

    Currently, this means an X or Type[X], where X is an instance or
    a type variable with an instance upper bound.
    """
    if isinstance(typ, TypeType):
        return supported_self_type(typ.item)
    if allow_callable and isinstance(typ, CallableType):
        # Special case: allow class callable instead of Type[...] as cls annotation,
        # as well as callable self for callback protocols.
        return True
    return isinstance(typ, TypeVarType) or (
        allow_instances and isinstance(typ, Instance) and typ != fill_typevars(typ.type)
    )

