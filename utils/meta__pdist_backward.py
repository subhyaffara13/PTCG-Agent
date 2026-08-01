
def meta__pdist_backward(grad: Tensor, self: Tensor, p: float, pdist: Tensor) -> Tensor:
    torch._check(
        self.is_contiguous(), lambda: "_pdist_backward requires self to be contiguous"
    )
    torch._check(
        pdist.is_contiguous(), lambda: "_pdist_backward requires pdist to be contiguous"
    )
    return torch.empty_like(self, memory_format=torch.legacy_contiguous_format)

