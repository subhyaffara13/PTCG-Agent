
def view_copy_dtype(
    self: torch.Tensor,
    dtype: torch.dtype,
) -> torch.Tensor:
    return self.clone().view(dtype)

