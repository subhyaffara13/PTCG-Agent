
def create_indices_fake(x) -> torch.Tensor:
    """Create a fake indices that is used for autotuning."""
    size = V.graph.sizevars.optimization_hints(x.get_size())
    indices = torch.arange(0, size[-1], dtype=x.get_dtype(), device=x.get_device())
    indices = indices.expand(size).contiguous()
    return indices

