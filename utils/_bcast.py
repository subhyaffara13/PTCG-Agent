from typing import Any

def _bcast(
    x: ir.Value | object,
    y: ir.Value | object,
    x_aval: ShapedAbstractValue,
    y_aval: ShapedAbstractValue,
    out_aval: ShapedAbstractValue,
    dynamic_shape_replacement_fn: DynamicShapeReplacementFn,
) -> tuple[ir.Value, ir.Value]:
  x_dtype = x_aval.dtype
  y_dtype = y_aval.dtype
  if y_aval.weak_type:
    y_dtype = x_aval.dtype
  elif x_aval.weak_type:
    x_dtype = y_aval.dtype
  if not isinstance(x, ir.Value):
    if (y_type := getattr(y, "type", None)) == ir.IndexType.get():
      mlir_type = y_type
    else:
      mlir_type = _dtype_to_ir_type(x_dtype)
    x = ir_constant(x, mlir_type)
  if not isinstance(y, ir.Value):
    if (x_type := getattr(x, "type", None)) == ir.IndexType.get():
      mlir_type = x_type
    else:
      mlir_type = _dtype_to_ir_type(y_dtype)
    y = ir_constant(y, mlir_type)
  if x_aval.shape != out_aval.shape:
    x_ty = ir.VectorType.get(
        dynamic_shape_replacement_fn(out_aval.shape),
        _dtype_to_ir_type(x_dtype))
    x = vector.broadcast(x_ty, x)
  if y_aval.shape != out_aval.shape:
    y_ty = ir.VectorType.get(
        dynamic_shape_replacement_fn(out_aval.shape),
        _dtype_to_ir_type(y_dtype))
    y = vector.broadcast(y_ty, y)
  return x, y


def _bcast(
    x: Any,
    y: Any,
    x_aval: ShapedAbstractValue,
    y_aval: ShapedAbstractValue,
    out_aval: ShapedAbstractValue,
) -> tuple[mgpu.FragmentedArray, mgpu.FragmentedArray]:
  if not isinstance(x, mgpu.FragmentedArray):
    x_dtype = x_aval.dtype
    if x_aval.weak_type:
      x_dtype = y_aval.dtype
    x = _ensure_fa(x, x_dtype)
  if not isinstance(y, mgpu.FragmentedArray):
    y_dtype = y_aval.dtype
    if y_aval.weak_type:
      y_dtype = x_aval.dtype
    y = _ensure_fa(y, y_dtype)
  if x_aval.shape != out_aval.shape:
    x = x.broadcast(out_aval.shape)
  if y_aval.shape != out_aval.shape:
    y = y.broadcast(out_aval.shape)
  return x, y


def _bcast(
    x: ir.Value,
    y: ir.Value,
    x_aval: jax_core.ShapedArray,
    y_aval: jax_core.ShapedArray,
    out_aval: jax_core.ShapedArray,
) -> tuple[ir.Value, ir.Value]:
  if isinstance(
      x, (np.ndarray, np.number, int, float, literals.TypedNdArray)
  ):
    x_dtype = x_aval.dtype
    if x_aval.weak_type:
      x_dtype = y_aval.dtype
    x = _ir_constant(x, _dtype_to_ir_type(x_dtype))
  if isinstance(
      y, (np.ndarray, np.number, int, float, literals.TypedNdArray)
  ):
    y_dtype = y_aval.dtype
    if y_aval.weak_type:
      y_dtype = x_aval.dtype
    y = _ir_constant(y, _dtype_to_ir_type(y_dtype))
  if x_aval.shape != out_aval.shape:
    x = _bcast_to(x, out_aval.shape)
  if y_aval.shape != out_aval.shape:
    y = _bcast_to(y, out_aval.shape)
  return x, y

