
def is_similar_constraints(x: list[Constraint], y: list[Constraint]) -> bool:
    """Check that two lists of constraints have similar structure.

    This means that each list has same type variable plus direction pairs (i.e we
    ignore the target). Except for constraints where target is Any type, there
    we ignore direction as well.
    """
    return _is_similar_constraints(x, y) and _is_similar_constraints(y, x)

