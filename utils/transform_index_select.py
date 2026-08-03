import copy

def transform_index_select(
    constraint: Constraint, counter: int
) -> tuple[Constraint, int]:
    """
    The constraints consider the given tensor size, checks if the index is valid
    and if so, generates a constraint for replacing the input dimension
    with the required dimension
    """
    if not isinstance(constraint, IndexSelect):
        raise TypeError(type(constraint))
    dims, counter = gen_tensor_dims(constraint.tensor_size, counter)
    is_valid_index = valid_index(constraint.index, dims)
    nat_constraints = gen_nat_constraints(dims)

    # if the index is valid then replace the input dimension with the new dimension
    # otherwise the dimension will not be replaced and the clause will contain False
    new_dims = copy.deepcopy(dims)
    if is_valid_index == T():
        new_dims[constraint.index] = constraint.dim_replace  # type: ignore[unsupported-operation]

    transformed_constraint = Conj(
        [
            BinConstraintT(constraint.input_var, TensorType(dims), op_eq),
            *nat_constraints,
            is_valid_index,
            BinConstraintT(constraint.output, TensorType(new_dims), op_eq),
        ]
    )

    # print(constraints)
    return transformed_constraint, counter

