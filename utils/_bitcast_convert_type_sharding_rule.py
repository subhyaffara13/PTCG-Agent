
def _bitcast_convert_type_sharding_rule(operand, *, new_dtype):
  old_dtype = operand.dtype

  old_nbits = dtypes.itemsize_bits(old_dtype)
  new_nbits = dtypes.itemsize_bits(new_dtype)

  if old_nbits == new_nbits:
    return operand.sharding
  elif old_nbits > new_nbits:
    return operand.sharding.update(spec=(*operand.sharding.spec, None))
  else:
    return operand.sharding.update(spec=operand.sharding.spec[:-1])

