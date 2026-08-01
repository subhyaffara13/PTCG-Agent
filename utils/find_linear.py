
def find_linear(c: Constraint) -> tuple[bool, TypeVarId | None]:
    """Find out if this constraint represent a linear relationship, return target id if yes."""
    if isinstance(c.origin_type_var, TypeVarType):
        if isinstance(c.target, TypeVarType):
            return True, c.target.id
    if isinstance(c.origin_type_var, ParamSpecType):
        if isinstance(c.target, ParamSpecType) and not c.target.prefix.arg_types:
            return True, c.target.id
    if isinstance(c.origin_type_var, TypeVarTupleType):
        target = get_proper_type(c.target)
        if isinstance(target, TupleType) and len(target.items) == 1:
            item = target.items[0]
            if isinstance(item, UnpackType) and isinstance(item.type, TypeVarTupleType):
                return True, item.type.id
    return False, None

