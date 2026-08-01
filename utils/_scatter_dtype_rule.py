
def _scatter_dtype_rule(operand, indices, updates, **kwargs):
  if not dtypes.issubdtype(indices.dtype, np.integer):
    raise ValueError("indices must have an integer type")
  lax.check_same_dtypes("scatter", operand, updates)
  return operand.dtype

