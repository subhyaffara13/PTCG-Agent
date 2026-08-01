
def _iota_meta(
    length: int,
    *,
    start: int,
    step: int,
    dtype: torch.dtype,
    device: torch.device,
    requires_grad: bool,
) -> TensorLikeType:
    torch._check(
        utils.is_integer_dtype(dtype),
        lambda: "prims.iota only supports integer dtypes",
    )
    torch._check(step != 0, lambda: "step must be nonzero")
    return torch.empty(
        length,
        dtype=dtype,
        device=device,
        requires_grad=requires_grad,
    )

