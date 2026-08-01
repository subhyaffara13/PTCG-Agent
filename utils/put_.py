
def put_(
    self: torch.Tensor,
    index: torch.Tensor,
    source: torch.Tensor,
    accumulate: bool = False,
) -> torch.Tensor:
    out = aten.put(self, index, source, accumulate=accumulate)
    return self.copy_(out)

