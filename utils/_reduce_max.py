
def _reduce_max(a: ArrayLike, axis: Axis = None, dtype: DTypeLike | None = None,
                out: None = None, keepdims: bool = False,
                initial: ArrayLike | None = None, where: ArrayLike | None = None) -> Array:
  return _reduction(a, "max", lax.max, -np.inf, has_identity=False,
                    axis=axis, dtype=dtype, out=out, keepdims=keepdims,
                    initial=initial, where_=where, parallel_reduce=lax_parallel.pmax)

