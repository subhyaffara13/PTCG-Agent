
def generate_calc_maxpool(
    constraint: Constraint, counter: int
) -> tuple[Constraint, int]:
    """
    Transform maxpool constraints
    """
    if not isinstance(constraint, CalcMaxPool):
        raise TypeError(type(constraint))
    d, counter = gen_tensor_dims(4, counter)
    maxpool_result = TensorType([d[0], d[1], d[2], d[3]])

    # the maxpool result is a tensor of size 4
    c1 = BinConstraintT(constraint.maxpool_result, maxpool_result, op_eq)

    # the input corresponds to the output in the first and second dimension of maxpool
    c2 = BinConstraintD(constraint.matching_constraint[1], d[1], op_eq)
    c3 = BinConstraintD(constraint.matching_constraint[0], d[0], op_eq)
    c4, c5 = calc_last_two_dims(constraint, d)

    leq_constraints = Conj(
        [
            BinConstraintD(0, d[0], op_leq),
            BinConstraintD(0, d[1], op_leq),
            BinConstraintD(0, d[2], op_leq),
            BinConstraintD(0, d[3], op_leq),
        ]
    )

    return Conj([c1, c2, c3, c4, c5, leq_constraints]), counter

