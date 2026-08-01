
def _uniform_aten(
    shape: ShapeType,
    *,
    low: float,
    high: float,
    dtype: torch.dtype,
    device: torch.device,
    stride: ShapeType,
    generator: torch.Generator | None = None,
) -> Tensor:
    a = torch.empty_strided(shape, stride=stride, dtype=dtype, device=device)
    a.uniform_(low, high, generator=generator)
    return a

