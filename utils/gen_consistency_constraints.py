
def gen_consistency_constraints(
    constraint: BinConstraintT, counter: int
) -> tuple[list[Constraint], int]:
    """
    Args:
        constraint: Consistency constraint on tensors
        counter: for variable tracking

    Returns: Equality and consistency constraints on dimensions

    """

    all_constraints: list[Constraint] = []

    for i in range(1, MAX_TENSOR_RANK + 1):
        new_dims_rhs_1, counter = gen_tensor_dims(i, counter)
        new_dims_rhs_2, counter = gen_tensor_dims(i, counter)

        nat_constraints = gen_nat_constraints(new_dims_rhs_1 + new_dims_rhs_2)

        c_tensor_i = Conj(
            [
                BinConstraintT(constraint.lhs, TensorType(new_dims_rhs_1), op_eq),
                BinConstraintT(constraint.rhs, TensorType(new_dims_rhs_2), op_eq),
            ]
            + [
                BinConstraintD(d1, d2, op_consistency)
                for d1, d2 in zip(new_dims_rhs_1, new_dims_rhs_2)
            ]
            + nat_constraints
        )

        all_constraints.append(c_tensor_i)

    return all_constraints, counter

