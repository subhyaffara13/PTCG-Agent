
def _argminmax_dtype_rule(operand, *, axes, index_dtype):
  if not dtypes.issubdtype(index_dtype, np.integer):
    raise TypeError("index_dtype must be an integer type, but got {}"
                    .format(dtype_to_string(index_dtype)))
  return index_dtype

