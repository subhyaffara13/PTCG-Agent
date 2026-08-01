
def dot_prepare(parts: list[DotPart], tensor_info: TensorInfo) -> torch.Tensor:
    """
    Prepare tensor for dot product by matching levels and reshaping.
    """
    new_levels = []
    needs_reshape = False

    for part in parts:
        if len(part.dims) != 1:
            needs_reshape = True
        new_levels.extend(part.dims)

    if tensor_info.tensor is None:
        raise RuntimeError("Cannot perform dot product on None tensor")
    result = _match_levels(tensor_info.tensor, tensor_info.levels, new_levels)

    if not needs_reshape:
        return result

    # Reshape for matrix operations
    view = [part.total_size for part in parts]
    return result.reshape(view)

