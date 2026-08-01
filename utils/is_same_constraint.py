
def is_same_constraint(c1: Constraint, c2: Constraint) -> bool:
    # Ignore direction when comparing constraints against Any.
    skip_op_check = isinstance(get_proper_type(c1.target), AnyType) and isinstance(
        get_proper_type(c2.target), AnyType
    )
    return (
        c1.type_var == c2.type_var
        and (c1.op == c2.op or skip_op_check)
        and mypy.subtypes.is_same_type(c1.target, c2.target)
    )

