
def meta__pdist_forward(self: Tensor, p: float = 2) -> Tensor:
    torch._check(
        self.is_contiguous(), lambda: "_pdist_forward requires contiguous input"
    )
    n = self.size(0)
    if n <= 1:
        return self.new_empty([0]).to(memory_format=torch.legacy_contiguous_format)  # type: ignore[call-overload]
    else:
        return self.new_empty((n * (n - 1) // 2,)).to(
            memory_format=torch.legacy_contiguous_format
        )  # type: ignore[call-overload]

