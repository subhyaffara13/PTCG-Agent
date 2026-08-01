
def _ensure_ir_value(x: Any, dtype: jnp.dtype) -> ir.Value:
  if isinstance(x, ir.Value):
    mlir_dtype = mgpu_utils.dtype_to_ir_type(dtype)
    if isinstance(x.type, ir.VectorType):
      assert ir.VectorType(x.type).element_type == mlir_dtype
    else:
      assert x.type == mlir_dtype, (x.type, mlir_dtype)
    return x
  elif isinstance(x, mgpu.FragmentedArray):
    assert x.mlir_dtype == mgpu_utils.dtype_to_ir_type(dtype)
    if isinstance(x.layout, mgpu.WGSplatFragLayout):
      return x.registers.item()
    raise NotImplementedError(f"Unsupported layout: {x.layout}")
  return _ir_constant(x, mgpu_utils.dtype_to_ir_type(dtype))


def _ensure_ir_value(x: object, aval: jax_core.ShapedArray) -> ir.Value:
  if isinstance(x, ir.Value):
    return x
  elif isinstance(
      x, (np.number, np.ndarray, int, float, literals.TypedNdArray)
  ):
    return _ir_constant(x, _dtype_to_ir_type(aval.dtype))
  raise NotImplementedError

