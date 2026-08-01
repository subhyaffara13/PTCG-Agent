
def erase_return_self_types(typ: Type, self_type: Instance) -> Type:
    """If a typ is function-like and returns self_type, replace return type with Any."""
    proper_type = get_proper_type(typ)
    if isinstance(proper_type, CallableType):
        ret = get_proper_type(proper_type.ret_type)
        if isinstance(ret, Instance) and ret == self_type:
            return proper_type.copy_modified(ret_type=AnyType(TypeOfAny.implementation_artifact))
    elif isinstance(proper_type, Overloaded):
        return Overloaded(
            [
                cast(CallableType, erase_return_self_types(it, self_type))
                for it in proper_type.items
            ]
        )
    return typ

