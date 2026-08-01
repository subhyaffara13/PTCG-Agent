
def generate_d_gub(constraint: Constraint, counter: int) -> tuple[Constraint, int]:
    """
    Transform greatest upper bound for dimensions into equality constraints
    """
    if not isinstance(constraint, DGreatestUpperBound):
        raise TypeError(type(constraint))
    c1 = Conj(
        [
            BinConstraintD(constraint.rhs1, Dyn, op_eq),
            BinConstraintD(constraint.res, constraint.rhs2, op_eq),
        ]
    )
    c2 = Conj(
        [
            BinConstraintD(constraint.rhs2, Dyn, op_eq),
            BinConstraintD(constraint.res, constraint.rhs1, op_eq),
        ]
    )
    c3 = Conj(
        [
            BinConstraintD(constraint.rhs2, constraint.rhs1, op_eq),
            BinConstraintD(constraint.res, constraint.rhs1, op_eq),
        ]
    )
    return Disj([c1, c2, c3]), counter

