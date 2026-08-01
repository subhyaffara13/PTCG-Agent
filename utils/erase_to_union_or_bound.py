
def erase_to_union_or_bound(typ: TypeVarType) -> ProperType:
    if typ.values:
        return make_simplified_union(typ.values)
    else:
        return get_proper_type(typ.upper_bound)

