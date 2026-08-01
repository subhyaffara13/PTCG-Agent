
def broadcast_dim(
    tensor_input1: Sequence[DVar | None],
    tensor_input2: Sequence[DVar],
    res1: Sequence[DVar],
    res2: Sequence[DVar],
    index: int,
    padding: bool = False,
) -> Constraint:
    """
    Apply broadcasting to the 'index' dimension of tensor_input1.
    Args:
        tensor_input1: should represent [d1, ..., d_index, ...] where d_index = 1
        tensor_input2: represents the second input
        res1: broadcasted result 1
        res2: broadcasted result 2
        index: the index to broadcast
        padding: If padding was used, then tensor_input1[index] does not exist

    Returns:

    """
    if tensor_input1[index] is None:
        if not padding:
            raise AssertionError("Expected padding when tensor_input1[index] is None")

    if not padding:
        # then the inputs are the same length so they all have dimensions at "index"
        return Conj(
            [
                BinConstraintD(tensor_input1[index], 1, op_eq),  # type: ignore[arg-type]
                BinConstraintD(res1[index], res2[index], op_eq),
                BinConstraintD(res2[index], tensor_input2[index], op_eq),
            ]
        )

    else:
        # we don't set the input dimension to 1, since it doesn't exist.
        return Conj(
            [
                BinConstraintD(res1[index], res2[index], op_eq),
                BinConstraintD(res2[index], tensor_input2[index], op_eq),
            ]
        )

