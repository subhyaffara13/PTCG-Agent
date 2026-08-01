
def erase_to_bound(t: Type) -> Type:
    # TODO: use value restrictions to produce a union?
    t = get_proper_type(t)
    if isinstance(t, TypeVarType):
        return t.upper_bound
    if isinstance(t, TypeType):
        if isinstance(t.item, TypeVarType):
            return TypeType.make_normalized(t.item.upper_bound, is_type_form=t.is_type_form)
    return t

