
def _mlir_type_to_numpy_dtype(type: ir.Type) -> np.dtype:
  """Converts an MLIR scalar type to a NumPy dtype."""

  if isinstance(type, ir.IntegerType):
    type = ir.IntegerType(type)
    width = type.width
    if width == 1:
      return np.dtype(np.bool_)
    elif width == 8:
      return np.dtype(np.uint8 if type.is_unsigned else np.int8)
    elif width == 16:
      return np.dtype(np.uint16 if type.is_unsigned else np.int16)
    elif width == 32:
      return np.dtype(np.uint32 if type.is_unsigned else np.int32)
    elif width == 64:
      return np.dtype(np.uint64 if type.is_unsigned else np.int64)
    else:
      raise ValueError(f"Unsupported integer width: {width}")

  elif isinstance(type, ir.F16Type):
    return np.dtype(np.float16)
  elif isinstance(type, ir.F32Type):
    return np.dtype(np.float32)
  elif isinstance(type, ir.F64Type):
    return np.dtype(np.float64)
  elif isinstance(type, ir.BF16Type):
    return np.dtype(ml_dtypes.bfloat16)

  elif isinstance(type, ir.ComplexType):
    element_type = ir.ComplexType(type).element_type
    if isinstance(element_type, ir.F32Type):
      return np.dtype(np.complex64)
    elif isinstance(element_type, ir.F64Type):
      return np.dtype(np.complex128)
    else:
      raise ValueError(f"Unsupported complex element type: {element_type}")

  else:
    raise TypeError(f"Unsupported MLIR type for NumPy conversion: {type}")

