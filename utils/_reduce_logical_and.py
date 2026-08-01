
def _reduce_logical_and(a: ArrayLike, axis: Axis = None, dtype: DTypeLike | None = None,
                        out: None = None, keepdims: bool = False,
                        initial: ArrayLike | None = None, where: ArrayLike | None = None) -> Array:
  return _reduction(a, name="reduce_logical_and", op=lax.bitwise_and, init_val=True, preproc=_cast_to_bool,
                    axis=_ensure_optional_axes(axis), dtype=dtype, out=out, keepdims=keepdims,
                    initial=initial, where_=where)

