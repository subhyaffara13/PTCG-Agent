
def _pad_dtype_rule(operand, padding_value, *, padding_config):
  if operand.dtype != padding_value.dtype:
    msg = "pad operand and padding_value must be same dtype: got {} and {}."
    raise TypeError(msg.format(operand.dtype, padding_value.dtype))

  return input_dtype(operand, padding_value)

