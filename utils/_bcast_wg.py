from typing import Any

def _bcast_wg(
    x: Any,
    y: Any,
    x_aval: ShapedAbstractValue,
    y_aval: ShapedAbstractValue,
    out_aval: ShapedAbstractValue,
) -> tuple[ir.Value, ir.Value]:
  """Ensures that ``x`` and ``y`` have the expected shapes and dtypes.

  More specifically, the inputs are converted to vectors of the same dtype
  as ``x_aval`` and ``y_aval``, and broadcasted to the output shape
  if necessary.
  """
  x_dtype = x_aval.dtype
  if not isinstance(x, ir.Value):
    if x_aval.weak_type:
      x_dtype = y_aval.dtype
    x = _ensure_ir_value(x, x_dtype)
  y_dtype = y_aval.dtype
  if not isinstance(y, ir.Value):
    if y_aval.weak_type:
      y_dtype = x_aval.dtype
    y = _ensure_ir_value(y, y_dtype)
  if not out_aval.shape:
    return x, y

  def bcast(value, dtype):
    ty = ir.VectorType.get(out_aval.shape, mgpu_utils.dtype_to_ir_type(dtype))
    if isinstance(value.type, ir.VectorType):
      assert value.type.rank == len(out_aval.shape), "broadcast ranks mismatch"
      dims = range(len(out_aval.shape))
      return mgpu.dialect.broadcast_in_dim(ty, value, dims)
    else:  # scalar broadcast
      return vector_dialect.broadcast(ty, value)

  if x_aval.shape != out_aval.shape:
    x = bcast(x, x_dtype)
  if y_aval.shape != out_aval.shape:
    y = bcast(y, y_dtype)
  return x, y

