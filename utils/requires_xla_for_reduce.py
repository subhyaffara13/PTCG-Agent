
def requires_xla_for_reduce(name, dtype):
  if name not in ["min", "max", "add"]:
    return True
  if name in ["min", "max"] and dtype in [
      np.bool_, np.uint32, np.uint64, np.complex64, np.complex128
  ]:
    return True
  if name == "min" and dtype in [np.uint8, np.uint16]:
    return True
  if name == "add" and dtype not in [
      dtypes.bfloat16, np.float16, np.float32, np.float64
  ]:
    return True
  return False

