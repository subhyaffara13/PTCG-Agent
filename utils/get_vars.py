
def get_vars(target: Type, vars: list[TypeVarId]) -> set[TypeVarId]:
    """Find type variables for which we are solving in a target type."""
    return {tv.id for tv in get_all_type_vars(target)} & set(vars)

