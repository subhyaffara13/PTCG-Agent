
def _uniform_helper(
    shape: ShapeType,
    low: bool | int | float = 0.0,
    high: bool | int | float = 1.0,
    *,
    stride: ShapeType,
    dtype: torch.dtype,
    device: DeviceLikeType,
) -> TensorLikeType:
    utils.validate_shape(shape)

    if not isinstance(low, Number):
        raise AssertionError(f"low must be Number, got {type(low)}")
    if not isinstance(high, Number):
        raise AssertionError(f"high must be Number, got {type(high)}")
    low = sym_float(low)
    high = sym_float(high)

    if not isinstance(dtype, torch.dtype):
        raise AssertionError(f"dtype must be torch.dtype, got {type(dtype)}")
    device = utils.canonicalize_device(device)

    return prims._uniform_helper(
        shape, low=low, high=high, dtype=dtype, device=device, stride=stride
    )

