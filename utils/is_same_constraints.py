
def is_same_constraints(x: list[Constraint], y: list[Constraint]) -> bool:
    for c1 in x:
        if not any(is_same_constraint(c1, c2) for c2 in y):
            return False
    for c1 in y:
        if not any(is_same_constraint(c1, c2) for c2 in x):
            return False
    return True

