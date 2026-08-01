
def primal_dtype_to_tangent_dtype(primal_dtype):
  if isinstance(primal_dtype, dtypes.ExtendedDType):
    return primal_dtype._rules.tangent_dtype(primal_dtype)
  elif not dtypes.issubdtype(primal_dtype, np.inexact):
    return dtypes.float0
  else:
    return primal_dtype

