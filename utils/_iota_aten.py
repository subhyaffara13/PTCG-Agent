
def _iota_aten(
    length: int,
    *,
    start: int,
    step: int,
    dtype: torch.dtype,
    device: torch.device,
    requires_grad: bool,
) -> TensorLikeType:
    end = start + length * step
    return torch.arange(
        start, end, step, dtype=dtype, device=device, requires_grad=requires_grad
    )

