
def _reduce_bitwise_and(a: ArrayLike, axis: Axis = None, dtype: DTypeLike | None = None,
                        out: None = None, keepdims: bool = False,
                        initial: ArrayLike | None = None, where: ArrayLike | None = None) -> Array:
  arr = lax.asarray(a)
  init_val = np.array(-1).astype(dtype or arr.dtype)
  return _reduction(arr, name="reduce_bitwise_and", op=lax.bitwise_and, init_val=init_val, preproc=_require_integer,
                    axis=_ensure_optional_axes(axis), dtype=dtype, out=out, keepdims=keepdims,
                    initial=initial, where_=where)

