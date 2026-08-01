
def _reduce_any(a: ArrayLike, axis: Axis = None, out: None = None,
                keepdims: bool = False, *, where: ArrayLike | None = None) -> Array:
  return _reduction(a, "any", lax.bitwise_or, False, preproc=_cast_to_bool,
                    axis=axis, out=out, keepdims=keepdims, where_=where)

