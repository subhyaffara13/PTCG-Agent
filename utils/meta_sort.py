
def meta_sort(self, stable=None, dim=-1, descending=False, values=None, indices=None):
    v, i = torch.empty_like(self), torch.empty_like(self, dtype=torch.int64)
    if values is not None and indices is not None:
        if not isinstance(values, TensorLike):
            raise AssertionError(f"values must be TensorLike, got {type(values)}")
        if not isinstance(indices, TensorLike):
            raise AssertionError(f"indices must be TensorLike, got {type(indices)}")
        # Makes sure values and indices have the same strides. For cases where
        # these have different shapes, like (5, 10, 5) and (0) in msort.
        out_shape = v.shape
        out_stride = v.stride()
        values = _maybe_resize_out(values, out_shape)
        indices = _maybe_resize_out(indices, out_shape)
        values.as_strided_(out_shape, out_stride)
        indices.as_strided_(out_shape, out_stride)
        _safe_copy_out(copy_from=v, copy_to=values)  # type: ignore[arg-type]
        _safe_copy_out(copy_from=i, copy_to=indices)  # type: ignore[arg-type]
        return values, indices
    return v, i

