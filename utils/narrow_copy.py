
def narrow_copy(
    self: torch.Tensor,
    dim: int,
    start: int,
    length: int,
) -> torch.Tensor:
    # Use memory_format=torch.contiguous_format to ensure correct strides.
    # For empty tensors, a plain clone() preserves the input view's strides.
    return torch.narrow(self, dim, start, length).clone(
        memory_format=torch.contiguous_format
    )

