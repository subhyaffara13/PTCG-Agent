
def calc_last_two_dims(
    constraint: CalcConv | CalcMaxPool, d: list[DVar]
) -> tuple[Constraint, Constraint]:
    """
    Generates constraints for the last two dimensions of a convolution or a maxpool output
    Args:
        constraint: CalcConv or CalcMaxPool
        d: The list of output dimensions

    Returns: Constraints for calculating the last two dimensions of the output

    """

    if not isinstance(constraint, (CalcConv, CalcMaxPool)):
        raise AssertionError(
            f"Expected CalcConv or CalcMaxPool, got {type(constraint)}"
        )

    b3 = constraint.matching_constraint[2]
    b4 = constraint.matching_constraint[3]

    b3_dyn = Conj([BinConstraintD(d[2], Dyn, op_eq), BinConstraintD(b3, Dyn, op_eq)])
    b4_dyn = Conj([BinConstraintD(d[3], Dyn, op_eq), BinConstraintD(b4, Dyn, op_eq)])

    d3_not_dyn = Conj(
        [BinConstraintD(d[2], Dyn, op_neq), BinConstraintD(b3, Dyn, op_neq)]
    )
    d4_not_dyn = Conj(
        [BinConstraintD(d[3], Dyn, op_neq), BinConstraintD(b4, Dyn, op_neq)]
    )

    # transform parameters into tuples in case they are not already
    padding = (
        (constraint.padding, constraint.padding)
        if isinstance(constraint.padding, int)
        else constraint.padding
    )
    kernel = (
        (constraint.kernel, constraint.kernel)
        if isinstance(constraint.kernel, int)
        else constraint.kernel
    )
    stride = (
        (constraint.stride, constraint.stride)
        if isinstance(constraint.stride, int)
        else constraint.stride
    )
    dilation = (
        (constraint.dilation, constraint.dilation)
        if isinstance(constraint.dilation, int)
        else constraint.dilation
    )

    f1 = BinConstraintD(b3, BinConstraintD(2, padding[0], op_mul), op_add)
    f2 = BinConstraintD(dilation[0], BinConstraintD(kernel[0], 1, op_sub), op_mul)
    f3 = BinConstraintD(
        BinConstraintD(BinConstraintD(f1, f2, op_sub), 1, op_sub), stride[0], op_div
    )
    f4 = BinConstraintD(f3, 1, op_add)

    c4 = Disj([b3_dyn, Conj([d3_not_dyn, BinConstraintD(d[2], f4, op_eq)])])

    f11 = BinConstraintD(b4, BinConstraintD(2, padding[1], op_mul), op_add)
    f22 = BinConstraintD(dilation[1], BinConstraintD(kernel[1], 1, op_sub), op_mul)
    f33 = BinConstraintD(
        BinConstraintD(BinConstraintD(f11, f22, op_sub), 1, op_sub), stride[1], op_div
    )
    f44 = BinConstraintD(f33, 1, op_add)

    c5 = Disj([b4_dyn, Conj([d4_not_dyn, BinConstraintD(d[3], f44, op_eq)])])

    return c4, c5

