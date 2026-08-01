
def _reduce_sum(a: ArrayLike, axis: Axis = None, dtype: DTypeLike | None = None,
                out: None = None, keepdims: bool = False,
                initial: ArrayLike | None = None, where: ArrayLike | None = None,
                promote_integers: bool = True) -> Array:
  return _reduction(a, "sum", lax.add, 0, preproc=_cast_to_numeric,
                    bool_op=lax.bitwise_or, upcast_f16_for_computation=(dtype is None),
                    axis=axis, dtype=dtype, out=out, keepdims=keepdims,
                    initial=initial, where_=where, parallel_reduce=lax_parallel.psum,
                    promote_integers=promote_integers)

