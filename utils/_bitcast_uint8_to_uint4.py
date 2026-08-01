
def _bitcast_uint8_to_uint4(operand):
  # Note: assumes little-endian byte order.
  assert operand.dtype == 'uint8'
  result = np.zeros((*operand.shape[:-1], operand.shape[-1] * 2), dtype='uint4')
  result[..., ::2] = (operand & 0b00001111).astype('uint4')
  result[..., 1::2] = ((operand & 0b11110000) >> 4).astype('uint4')
  return result

