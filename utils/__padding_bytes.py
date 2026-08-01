
def _PaddingBytes(buf_size, scalar_size):
  # ((buf_size + (scalar_size - 1)) // scalar_size) * scalar_size - buf_size
  return -buf_size & (scalar_size - 1)

