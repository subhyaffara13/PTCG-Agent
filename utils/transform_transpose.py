
def transform_transpose(constraint: Constraint, counter: int) -> tuple[Constraint, int]:
    """
    Similar to a sequence of two index-selects
    """
    if not isinstance(constraint, Transpose):
        raise TypeError(type(constraint))
    dims, counter = gen_tensor_dims(constraint.tensor_size, counter)
    is_valid_index1 = valid_index(constraint.index1, dims)
    is_valid_index2 = valid_index(constraint.index2, dims)
    new_dims = copy.deepcopy(dims)
    nat_constraints = gen_nat_constraints(dims)

    if is_valid_index1 == T() and is_valid_index2 == T():
        new_dims[constraint.index1] = dims[constraint.index2]
        new_dims[constraint.index2] = dims[constraint.index1]

    transformed_constraint = Conj(
        [
            BinConstraintT(constraint.input_var, TensorType(dims), op_eq),
            *nat_constraints,
            is_valid_index1,
            is_valid_index2,
            BinConstraintT(constraint.output, TensorType(new_dims), op_eq),
        ]
    )
    return transformed_constraint, counter

