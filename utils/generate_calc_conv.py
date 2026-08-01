
def generate_calc_conv(constraint: Constraint, counter: int) -> tuple[Constraint, int]:
    if not isinstance(constraint, CalcConv):
        raise TypeError(type(constraint))
    d, counter = gen_tensor_dims(4, counter)
    conv_result = TensorType([d[0], d[1], d[2], d[3]])

    # the convolution result is a tensor of size 4
    c1 = BinConstraintT(constraint.conv_result, conv_result, op_eq)

    # the second dimension of the output is equal to the output channels
    c2 = Conj(
        [
            BinConstraintD(d[1], constraint.c_out, op_eq),
            BinConstraintD(d[1], Dyn, op_neq),
        ]
    )

    # the input corresponds to the output in the first dimension of the convolution
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

