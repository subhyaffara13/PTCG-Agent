
def _var_promote_types(a_dtype: DTypeLike, dtype: DTypeLike | None) -> tuple[DType, DType]:
  if dtype:
    if (not dtypes.issubdtype(dtype, np.complexfloating) and
        dtypes.issubdtype(a_dtype, np.complexfloating)):
      msg = ("jax.numpy.var does not yet support real dtype parameters when "
             "computing the variance of an array of complex values. The "
             "semantics of numpy.var seem unclear in this case. Please comment "
             "on https://github.com/jax-ml/jax/issues/2283 if this behavior is "
             "important to you.")
      raise ValueError(msg)
    computation_dtype = dtype
  else:
    if not dtypes.issubdtype(a_dtype, np.inexact):
      dtype = dtypes.to_inexact_dtype(a_dtype)
      computation_dtype = dtype
    else:
      dtype = np.array(0, a_dtype).real.dtype
      computation_dtype = a_dtype
  return _upcast_f16(computation_dtype), np.dtype(dtype)

