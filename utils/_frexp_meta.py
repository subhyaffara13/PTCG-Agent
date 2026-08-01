
def _frexp_meta(self: TensorLikeType) -> tuple[TensorLikeType, TensorLikeType]:
    torch._check(
        self.dtype.is_floating_point,
        lambda: "torch.frexp() only supports floating-point dtypes",
    )
    return torch.empty_like(self), torch.empty_like(self, dtype=torch.int32)

