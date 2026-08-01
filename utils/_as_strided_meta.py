
def _as_strided_meta(
    a: TensorLikeType, size: ShapeType, stride: StrideType, storage_offset: int
) -> TensorLikeType:
    if len(size) != len(stride):
        raise AssertionError(f"len(size)={len(size)} != len(stride)={len(stride)}")
    if storage_offset < 0:
        raise AssertionError(f"storage_offset must be >= 0, got {storage_offset}")
    utils.validate_strides(stride)
    utils.validate_shape(size)

    if reduce(operator.mul, size) == 0:
        # NOTE: This special case is to avoid having to acquire the storage below
        # as_strided to shapes with no elements are trivially valid, so it's OK
        pass
    elif isinstance(a, torch.Tensor):
        utils.check_in_bounds_for_storage(
            a._typed_storage(), size, stride, storage_offset
        )

    return torch.as_strided(a, size, stride, storage_offset)

