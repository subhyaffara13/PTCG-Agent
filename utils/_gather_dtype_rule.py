
def _gather_dtype_rule(operand, indices, *, fill_value, **kwargs):
  if not dtypes.issubdtype(indices.dtype, np.integer):
    raise ValueError("indices must have an integer type")
  return operand.dtype

