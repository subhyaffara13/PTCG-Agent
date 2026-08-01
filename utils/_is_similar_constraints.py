
def _is_similar_constraints(x: list[Constraint], y: list[Constraint]) -> bool:
    """Check that every constraint in the first list has a similar one in the second.

    See docstring above for definition of similarity.
    """
    for c1 in x:
        has_similar = False
        for c2 in y:
            # Ignore direction when either constraint is against Any.
            skip_op_check = isinstance(get_proper_type(c1.target), AnyType) or isinstance(
                get_proper_type(c2.target), AnyType
            )
            if c1.type_var == c2.type_var and (c1.op == c2.op or skip_op_check):
                has_similar = True
                break
        if not has_similar:
            return False
    return True

