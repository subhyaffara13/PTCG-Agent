
def gen_lists_of_dims(
    num_tensors: int, dim_size: int, counter: int
) -> tuple[list[list[DVar]], int]:
    """
    Generate lists of DVar to represent tensor dimensions
    Args:
        num_tensors: the required number of tensors
        dim_size: the number of dimensions for each tensor
        counter: variable tracking

    Returns: A list of a list of tensor dimensions

    """
    res = []

    for _ in range(num_tensors):
        dims, counter = gen_tensor_dims(dim_size, counter)
        res.append(dims)

    return res, counter

