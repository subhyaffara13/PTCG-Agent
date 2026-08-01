
def _collapse_view_meta(a: TensorLikeType, start: int, end: int) -> TensorLikeType:
    new_shape, new_strides = _collapse_view_helper(
        a, start, end, "Attempting to view a collapsed tensor, but no such view exists!"
    )
    if new_strides is None:
        raise AssertionError(
            "new_strides should not be None after _collapse_view_helper"
        )
    if new_shape is None:
        raise AssertionError("new_shape should not be None after _collapse_view_helper")
    return a.as_strided(new_shape, new_strides, a.storage_offset())

