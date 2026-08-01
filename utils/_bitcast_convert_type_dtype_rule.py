
def _bitcast_convert_type_dtype_rule(operand, *, new_dtype):
  old_dtype = operand.dtype
  if (dtypes.issubdtype(old_dtype, np.bool_) or
      dtypes.issubdtype(old_dtype, np.complexfloating) or
      dtypes.issubdtype(new_dtype, np.bool_) or
      dtypes.issubdtype(new_dtype, np.complexfloating)):
    if old_dtype != new_dtype:
      raise TypeError("lax.bitcast_convert_type does not support bool or complex values "
                      "unless the operand and destination types match. "
                      f"Got operand dtype={old_dtype}, {new_dtype=}. "
                      "Consider using the arr.view() method instead.")
  return new_dtype

