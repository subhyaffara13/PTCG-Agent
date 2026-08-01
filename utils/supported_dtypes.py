
def supported_dtypes() -> set[DTypeLike]:
  types: set[DTypeLike]
  if device_under_test() == "tpu":
    types = {np.bool_, _dtypes.int4, np.int8, np.int16, np.int32,
             _dtypes.uint4, np.uint8, np.uint16, np.uint32,
             _dtypes.bfloat16, np.float16, np.float32, np.complex64,
             _dtypes.float8_e4m3fn, _dtypes.float8_e4m3b11fnuz,
             _dtypes.float8_e5m2}
  elif device_under_test() == "gpu":
    types = {np.bool_, np.int8, np.int16, np.int32, np.int64,
             np.uint8, np.uint16, np.uint32, np.uint64,
             _dtypes.bfloat16, np.float16, np.float32, np.float64,
             np.complex64, np.complex128, _dtypes.float8_e4m3fn,
             _dtypes.float8_e5m2}
  else:
    types = {np.bool_, _dtypes.int4, np.int8, np.int16, np.int32, np.int64,
             _dtypes.uint4, np.uint8, np.uint16, np.uint32, np.uint64,
             _dtypes.bfloat16, np.float16, np.float32, np.float64,
             np.complex64, np.complex128}
  if not config.enable_x64.value:
    types -= {np.uint64, np.int64, np.float64, np.complex128}
  return types

