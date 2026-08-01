
def _get_expected_num_tensor_outputs(op: OpOverload) -> int | None:
    """
    Get the expected number of tensor outputs for an operator based on its schema.

    Returns:
        The number of tensor outputs expected. Returns 0 for ops that don't return tensors
        (e.g., _linalg_check_errors). Returns 1 for single tensor return, and >1 for
        tuple returns where each element is a tensor. Returns None for List[Tensor]
        returns where the length is unknown at schema time.
    """
    return_types = op._schema.returns
    if len(return_types) == 0:
        return 0

    first_return = return_types[0]
    if isinstance(first_return.type, torch.TensorType):
        # Could be single tensor or tuple of tensors
        return len(return_types)
    elif isinstance(first_return.type, torch.ListType):
        # List[Tensor] - we don't know the length at schema time
        return None
    else:
        # Not a tensor return type
        return 0

