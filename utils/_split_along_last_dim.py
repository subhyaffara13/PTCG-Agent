
def _split_along_last_dim(x, world_size):
    """Split tensor along last dimension into world_size chunks."""
    return torch.chunk(x, world_size, dim=-1)

