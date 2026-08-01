
def meta_index_reduce(
    self: Tensor,
    dim: int,
    index: Tensor,
    source: torch.Tensor,
    reduce: str,
    *,
    include_self: bool = True,
) -> Tensor:
    return torch.empty_like(self, memory_format=torch.contiguous_format)

