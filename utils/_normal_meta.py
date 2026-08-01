
def _normal_meta(
    shape: ShapeType,
    *,
    mean: float | complex,
    std: float,
    dtype: torch.dtype,
    device: torch.device,
    requires_grad: bool,
    generator: torch.Generator | None = None,
) -> TensorLikeType:
    torch._check(
        std >= 0.0,
        lambda: f"expected non-negative standard deviation, but got std={std}",
    )

    torch._check(
        utils.is_float_dtype(dtype) or utils.is_complex_dtype(dtype),
        lambda: f"expected a floating-point or complex dtype, but got dtype={dtype}",
    )

    strides = utils.make_contiguous_strides_for(shape)
    return TensorMeta(shape=shape, strides=strides, dtype=dtype, device=device)

