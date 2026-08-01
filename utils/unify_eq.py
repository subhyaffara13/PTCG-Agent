
def unify_eq(list_of_eq):
    """
    Apply unification to a set of
    equality constraints
    """
    lhs, rhs = convert_eq(list_of_eq)
    return unify(lhs, rhs)

