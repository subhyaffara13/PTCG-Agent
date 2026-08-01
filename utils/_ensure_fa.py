
def _ensure_fa(x: object, dtype: jnp.dtype) -> mgpu.FragmentedArray:
  if isinstance(x, mgpu.FragmentedArray):
    assert x.mlir_dtype == mgpu_utils.dtype_to_ir_type(dtype)
    return x
  return mgpu.FragmentedArray.splat(
      _ensure_ir_value(x, dtype), (), is_signed=mgpu_utils.is_signed(dtype)
  )

