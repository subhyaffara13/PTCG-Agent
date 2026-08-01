
def _get_expected_shape(
    local_tensor: torch.Tensor, dim: int | None, keepdim: bool
) -> torch.Size:
    """Compute the expected output shape after reduction."""
    input_shape = list(local_tensor.shape)
    if dim is None:
        expected_shape = (
            torch.Size([1] * len(input_shape)) if keepdim else torch.Size([])
        )
    elif keepdim:
        if input_shape:
            input_shape[dim] = 1
        expected_shape = torch.Size(input_shape)
    else:
        if input_shape:
            input_shape.pop(dim)
        expected_shape = torch.Size(input_shape)

    return expected_shape

