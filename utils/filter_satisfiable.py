
def filter_satisfiable(option: list[Constraint] | None) -> list[Constraint] | None:
    """Keep only constraints that can possibly be satisfied.

    Currently, we filter out constraints where target is not a subtype of the upper bound.
    Since those can be never satisfied. We may add more cases in future if it improves type
    inference.
    """
    if not option:
        return option

    satisfiable = []
    for c in option:
        if isinstance(c.origin_type_var, TypeVarType) and c.origin_type_var.values:
            if any(
                mypy.subtypes.is_subtype(c.target, value) for value in c.origin_type_var.values
            ):
                satisfiable.append(c)
        elif mypy.subtypes.is_subtype(c.target, c.origin_type_var.upper_bound):
            satisfiable.append(c)
    if not satisfiable:
        return None
    return satisfiable

