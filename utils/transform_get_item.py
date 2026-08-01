
def transform_get_item(constraint: Constraint, counter: int) -> tuple[Constraint, int]:
    """
    generate an equality of the form:
    t = [a1, ..., an]
    then generate constraints that check if the given index is valid
    given this particular tensor size.
    If the index is valid, generate a constraint to get the item
    Note that we already handled the Dyn input case in the previous
    step.
    Args:
        constraint: GetItem which assumes we are getting an item from a tensor (not Dyn)
        counter: variable tracking
    Returns: simplified constraints for GetItem

    """
    if not isinstance(constraint, GetItem):
        raise TypeError(type(constraint))
    dims, counter = gen_tensor_dims(constraint.tensor_size, counter)
    nat_constraints = gen_nat_constraints(dims)

    is_valid_index = valid_index(constraint.index, dims)

    all_constraints = [
        BinConstraintT(constraint.input_var, TensorType(dims), op_eq),
        *nat_constraints,
        is_valid_index,
    ]

    # if the index is valid, we generate a constraint for getting an item
    # otherwise this clause will have been UNSAT due to the wrong index
    if is_valid_index == T():
        all_constraints.append(
            BinConstraintD(constraint.res, dims[constraint.index], op_eq)
        )

    return Conj(all_constraints), counter

