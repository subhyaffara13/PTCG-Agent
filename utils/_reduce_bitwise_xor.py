
def _reduce_bitwise_xor(a: ArrayLike, axis: Axis = None, dtype: DTypeLike | None = None,
                        out: None = None, keepdims: bool = False,
                        initial: ArrayLike | None = None, where: ArrayLike | None = None) -> Array:
  return _reduction(a, name="reduce_bitwise_xor", op=lax.bitwise_xor, init_val=0, preproc=_require_integer,
                    axis=_ensure_optional_axes(axis), dtype=dtype, out=out, keepdims=keepdims,
                    initial=initial, where_=where)

