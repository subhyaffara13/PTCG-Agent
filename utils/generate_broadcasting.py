
def generate_broadcasting(
    constraint: Constraint, counter: int
) -> tuple[Constraint, int]:
    """
    Transform broadcasting constraints
    """
    if not isinstance(constraint, ApplyBroadcasting):
        raise TypeError(type(constraint))
    e11, e12 = constraint.res1, constraint.res2
    e1, e2 = constraint.input1, constraint.input2

    e1_dyn = BinConstraintT(e1, Dyn, op_eq)
    e2_dyn = BinConstraintT(e2, Dyn, op_eq)

    # Introduce dimensions
    e1_equal_e11 = BinConstraintT(e1, e11, op_eq)
    e2_equal_e12 = BinConstraintT(e2, e12, op_eq)

    # dyn possibility
    e1_dyn_constraint = Conj([e1_dyn, e1_equal_e11, e2_equal_e12])
    e2_dyn_constraint = Conj([e2_dyn, e1_equal_e11, e2_equal_e12])

    # tensor possibility
    # generate dimensions to create tensors of size 1
    final_tensor_1_constraint, _, _, nat_dims_1, counter = gen_broadcasting_constraints(
        e1, e2, e11, e12, 1, counter
    )

    # generate dimensions to create tensors of size 2
    (
        final_tensor_2_constraint_no_padding,
        final_tensor_2_constraint_padding_arg1,
        final_tensor_2_constraint_padding_arg2,
        nat_dims_2,
        counter,
    ) = gen_broadcasting_constraints(e1, e2, e11, e12, 2, counter)

    # generate dimensions to create tensors of size 3
    (
        final_tensor_3_constraint_no_padding,
        final_tensor_3_constraint_padding_arg1,
        final_tensor_3_constraint_padding_arg2,
        nat_dims_3,
        counter,
    ) = gen_broadcasting_constraints(e1, e2, e11, e12, 3, counter)

    # generate dimensions to create tensors of size 4
    (
        final_tensor_4_constraint_no_padding,
        final_tensor_4_constraint_padding_arg1,
        final_tensor_4_constraint_padding_arg2,
        nat_dims_4,
        counter,
    ) = gen_broadcasting_constraints(e1, e2, e11, e12, 4, counter)

    final_result = Disj(
        [
            e1_dyn_constraint,
            e2_dyn_constraint,
            final_tensor_1_constraint,
            final_tensor_2_constraint_no_padding,
            final_tensor_2_constraint_padding_arg1,
            final_tensor_2_constraint_padding_arg2,
            final_tensor_3_constraint_no_padding,
            final_tensor_3_constraint_padding_arg1,
            final_tensor_3_constraint_padding_arg2,
            final_tensor_4_constraint_no_padding,
            final_tensor_4_constraint_padding_arg1,
            final_tensor_4_constraint_padding_arg2,
        ]
    )

    return (
        Conj([final_result, *nat_dims_1, *nat_dims_2, *nat_dims_3, *nat_dims_4]),
        counter,
    )

