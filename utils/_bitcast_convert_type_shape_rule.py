
def _bitcast_convert_type_shape_rule(operand, *, new_dtype):
  old_dtype = operand.dtype

  old_nbits = dtypes.itemsize_bits(old_dtype)
  new_nbits = dtypes.itemsize_bits(new_dtype)

  if old_nbits == new_nbits:
    return operand.shape
  elif old_nbits > new_nbits:
    return (*operand.shape, old_nbits // new_nbits)
  else:
    dim_size = operand.shape[-1] if operand.shape else 1
    if dim_size * old_nbits != new_nbits:
      raise ValueError(
        f"Attempting to convert array of shape {operand.shape} "
        f"from {old_dtype} of size {old_nbits} bits "
        f"to {new_dtype} of size {new_nbits}, bits "
        f"but {dim_size} * {old_nbits} != {new_nbits}")
    return operand.shape[:-1]

