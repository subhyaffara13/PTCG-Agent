
def generate_gub(constraint: Constraint, counter: int) -> tuple[Constraint, int]:
    """
    Transform greatest upper bound for tensors. Results in equality and Greatest Upper Bound
    on dimensions
    """
    if not isinstance(constraint, TGreatestUpperBound):
        raise TypeError(type(constraint))
    c1 = Conj(
        [
            Disj(
                [
                    BinConstraintT(constraint.rhs1, Dyn, op_eq),
                    BinConstraintT(constraint.rhs2, Dyn, op_eq),
                ]
            ),
            BinConstraintT(constraint.res, Dyn, op_eq),
        ]
    )

    [c2, c3, c4, c5], counter = gen_greatest_upper_bound(constraint, counter)

    return Disj([c1, c2, c3, c4, c5]), counter

