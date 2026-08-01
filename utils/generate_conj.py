
def generate_conj(constraint: Constraint, counter: int) -> tuple[Constraint, int]:
    """
    Transform conjunctions
    """
    if not isinstance(constraint, Conj):
        raise TypeError(type(constraint))
    new = []
    for c in constraint.conjucts:
        new_c, counter = transform_constraint(c, counter)
        new.append(new_c)
    return Conj(new), counter

