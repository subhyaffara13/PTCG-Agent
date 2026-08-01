
def _split_dim_meta(a: TensorLikeType, dim: int, outer_length: int) -> TensorLikeType:
    if not isinstance(a, TensorLike):
        raise AssertionError(f"a must be TensorLike, got {type(a)}")  # mypy
    utils.validate_idx(a.ndim, dim)
    utils.validate_dim_length(outer_length)

    # Verifies the dim can be split with the specified lhs_length
    inner_length = a.shape[dim] // outer_length

    if (a.shape[dim] % outer_length) != 0:
        msg = (
            f"Attempting to split dimension of length {a.shape[dim]}, "
            f"but outer length of {outer_length} divides it with a remainder!"
        )
        raise ValueError(msg)

    new_shape: list[int] = []
    new_strides: list[int] = []
    for idx in range(a.ndim):
        if idx == dim:
            new_shape.extend((outer_length, inner_length))
            new_strides.extend((a.stride()[idx] * inner_length, a.stride()[idx]))
        else:
            new_shape.append(a.shape[idx])
            new_strides.append(a.stride()[idx])

    return a.as_strided(new_shape, new_strides, a.storage_offset())

