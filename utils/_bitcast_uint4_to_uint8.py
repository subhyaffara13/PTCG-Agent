
def _bitcast_uint4_to_uint8(operand):
  # Note: assumes little-endian byte order.
  assert operand.dtype == 'uint4'
  operand = operand.astype('uint8')
  return operand[..., ::2] + (operand[..., 1::2] << 4)

