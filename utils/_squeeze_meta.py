
def _squeeze_meta(a: TensorLikeType, dimensions: Sequence) -> TensorLikeType:
    if not isinstance(a, TensorLike):
        raise AssertionError(f"a must be TensorLike, got {type(a)}")  # mypy

    for idx in dimensions:
        utils.validate_idx(a.ndim, idx)
        if a.shape[idx] != 1:
            raise AssertionError(
                f"Cannot squeeze dimension {idx} with size {a.shape[idx]} (must be 1)"
            )

    new_shape = []
    new_strides = []
    for idx in range(len(a.shape)):
        if idx in dimensions:
            continue

        new_shape.append(a.shape[idx])
        new_strides.append(a.stride()[idx])

    return a.as_strided(new_shape, new_strides, a.storage_offset())

