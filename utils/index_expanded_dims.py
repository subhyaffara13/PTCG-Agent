
def index_expanded_dims(t: torch.Tensor, expanded_dims: list[int]) -> torch.Tensor:
    for expanded_dim in expanded_dims:
        t = torch.ops.aten.slice(t, expanded_dim, 0, 1)
    return t

