
def get_dtype_packing(dtype):
  bits = dtypes.itemsize_bits(dtype)
  return 32 // bits

