
def strip_type(typ: Type) -> Type:
    """Make a copy of type without 'debugging info' (function name)."""
    orig_typ = typ
    typ = get_proper_type(typ)
    if isinstance(typ, CallableType):
        return typ.copy_modified(name=None)
    elif isinstance(typ, Overloaded):
        return Overloaded([cast(CallableType, strip_type(item)) for item in typ.items])
    else:
        return orig_typ

