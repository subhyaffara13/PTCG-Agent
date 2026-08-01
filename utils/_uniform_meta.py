
def _uniform_meta(
    shape: ShapeType,
    *,
    low: float,
    high: float,
    dtype: torch.dtype,
    device: torch.device,
    stride: ShapeType,
    generator: torch.Generator | None = None,
) -> TensorLikeType:
    return TensorMeta(shape=shape, strides=stride, dtype=dtype, device=device)

