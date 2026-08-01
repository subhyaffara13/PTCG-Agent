
def generate_disj(constraint: Constraint, counter: int) -> tuple[Constraint, int]:
    """
    Transform disjunctions
    """
    if not isinstance(constraint, Disj):
        raise TypeError(type(constraint))
    new = []
    for c in constraint.disjuncts:
        new_c, counter = transform_constraint(c, counter)
        new.append(new_c)
    return Disj(new), counter

