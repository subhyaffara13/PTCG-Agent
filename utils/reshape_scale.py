
def reshape_scale(scale: torch.Tensor, axis: int, input: torch.Tensor) -> torch.Tensor:
    """Reshapes the scale so that we can multiply it to the input by the given axis."""
    new_shape = [1] * input.ndim
    new_shape[axis] = input.size(axis)
    return scale.view(new_shape)

