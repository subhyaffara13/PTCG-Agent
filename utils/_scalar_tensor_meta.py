
def _scalar_tensor_meta(
    scalar: NumberType,
    *,
    dtype: torch.dtype,
    device: torch.device,
) -> TensorLikeType:
    shape: ShapeType = []
    strides = utils.make_contiguous_strides_for(shape)
    return TensorMeta(scalar, shape=shape, strides=strides, dtype=dtype, device=device)

