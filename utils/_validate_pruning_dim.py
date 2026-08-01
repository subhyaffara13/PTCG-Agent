
def _validate_pruning_dim(t, dim) -> None:
    r"""Validate that the pruning dimension is within the bounds of the tensor dimension.

    Args:
        t (torch.Tensor): tensor representing the parameter to prune
        dim (int): index of the dim along which we define channels to prune
    """
    if dim >= t.dim():
        raise IndexError(f"Invalid index {dim} for tensor of size {t.shape}")

