
def _ensure_mlir_value(val: object, aval: ShapedAbstractValue) -> Any:
  if isinstance(val, ir.Value):
    return val
  if isinstance(val, KeyScalarBundle):
    # TODO(slebedev): Drop this branch and change the return type to ir.Value.
    return val
  elif isinstance(val, (np.generic, np.ndarray, int, float)):
    return ir_constant(val, _dtype_to_ir_type(aval.dtype))
  else:
    raise RuntimeError(
        f"Unsupported argument to a JAX primitive of type: {type(val)}"
    )

