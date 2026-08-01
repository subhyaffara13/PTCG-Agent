
def _prod_aten(
    inp: TensorLikeType,
    dims: DimsSequenceType | None,
    *,
    dtype: torch.dtype | None = None,
) -> Tensor:
    if dims is not None:
        if len(dims) == 0:
            return inp.clone()
        for d in sorted(dims, reverse=True):
            if d < 0:
                raise AssertionError(f"dimension must be non-negative, got {d}")
            inp = torch.prod(inp, d, dtype=dtype)
        return inp
    else:
        return torch.prod(inp, dims, dtype=dtype)

