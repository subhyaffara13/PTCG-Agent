
def shallow_erase_type_for_equality(typ: Type) -> ProperType:
    """Erase type variables from Instance's"""
    p_typ = get_proper_type(typ)
    if isinstance(p_typ, Instance):
        if not p_typ.args:
            return p_typ
        args = erased_vars(p_typ.type.defn.type_vars, TypeOfAny.special_form)
        return Instance(p_typ.type, args, p_typ.line)
    if isinstance(p_typ, UnionType):
        items = [shallow_erase_type_for_equality(item) for item in p_typ.items]
        return UnionType.make_union(items)
    return p_typ

