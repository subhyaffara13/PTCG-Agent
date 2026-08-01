
def transform_constraint(
    constraint: Constraint, counter: int
) -> tuple[Constraint, int]:
    """
    Transforms a constraint into a simpler constraint.
    Ex: precision and consistency are transformed to equality
    Args:
        constraint: constraint to be transformed
        counter: for variable tracking

    Returns: Constraint

    """
    if type(constraint) in _TRANSFORMATION_RULES:
        return _TRANSFORMATION_RULES[type(constraint)](constraint, counter)

    else:
        return constraint, counter

