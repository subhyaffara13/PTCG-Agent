
def remove_optional(typ: Type) -> Type:
    typ = get_proper_type(typ)
    if isinstance(typ, UnionType):
        return UnionType.make_union(
            [t for t in typ.items if not isinstance(get_proper_type(t), NoneType)]
        )
    elif isinstance(typ, NoneType):
        return UninhabitedType()
    else:
        return typ

