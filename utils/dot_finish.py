
def dot_finish(parts: list[DotPart], result_tensor: torch.Tensor) -> Tensor:
    """
    Finish dot product by reshaping result and creating Tensor.
    """
    result_levels = []
    needs_reshape = False

    for part in parts:
        if len(part.dims) != 1:
            needs_reshape = True
        result_levels.extend(part.dims)

    if needs_reshape:
        new_size = []
        for level in result_levels:
            new_size.append(level.dim().size)
        result_tensor = result_tensor.reshape(new_size)

    tensor_result = Tensor.from_positional(result_tensor, result_levels, True)
    return tensor_result  # type: ignore[return-value]

