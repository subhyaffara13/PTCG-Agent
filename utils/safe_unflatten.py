
def safe_unflatten(tensor: torch.Tensor, dim: int, shape: torch.Size) -> torch.Tensor:
    if len(shape) == 0:
        if tensor.shape[dim] != 1:
            raise AssertionError(
                f"expected tensor.shape[{dim}] to be 1, got {tensor.shape[dim]}"
            )
        return tensor.squeeze(dim)
    return tensor.unflatten(dim, shape)

