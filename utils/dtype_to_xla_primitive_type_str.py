
def dtype_to_xla_primitive_type_str(dtype: np.dtype) -> str:
  """Converts a numpy dtype to an xla PrimitiveType."""
  if dtype == np.dtype("bfloat16"):
    return "BF16"
  elif dtype == np.dtype("float32"):
    return "F32"
  elif dtype == np.dtype("float64"):
    return "F64"
  elif dtype == np.dtype("int8"):
    return "S8"
  elif dtype == np.dtype("int16"):
    return "S16"
  elif dtype == np.dtype("int32"):
    return "S32"
  elif dtype == np.dtype("int64"):
    return "S64"
  elif dtype == np.dtype("uint8"):
    return "U8"
  elif dtype == np.dtype("uint16"):
    return "U16"
  elif dtype == np.dtype("uint32"):
    return "U32"
  elif dtype == np.dtype("uint64"):
    return "U64"
  else:
    raise ValueError(f"Unsupported dtype: {dtype}")

