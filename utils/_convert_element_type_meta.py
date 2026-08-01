
def _convert_element_type_meta(a: TensorLikeType, dtype: torch.dtype) -> TensorLikeType:
    # Type checks
    if not isinstance(a, TensorLike):
        raise AssertionError(f"a must be TensorLike, got {type(a)}")  # mypy
    if not isinstance(dtype, torch.dtype):
        raise AssertionError(f"dtype must be torch.dtype, got {type(dtype)}")

    # dtype conversion preserves dense strides
    if torch._prims_common.is_non_overlapping_and_dense_or_false(a):
        strides = a.stride()
    else:
        strides = utils.compute_elementwise_output_strides(a)

    return TensorMeta(a, strides=strides, dtype=dtype)

