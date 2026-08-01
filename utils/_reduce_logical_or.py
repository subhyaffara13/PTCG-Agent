
def _reduce_logical_or(a: ArrayLike, axis: Axis = None, dtype: DTypeLike | None = None,
                       out: None = None, keepdims: bool = False,
                       initial: ArrayLike | None = None, where: ArrayLike | None = None) -> Array:
  return _reduction(a, name="reduce_logical_or", op=lax.bitwise_or, init_val=False, preproc=_cast_to_bool,
                    axis=_ensure_optional_axes(axis), dtype=dtype, out=out, keepdims=keepdims,
                    initial=initial, where_=where)

