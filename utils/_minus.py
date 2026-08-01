
def _minus(x: ir.Value) -> ir.Value:
  if _is_triton_pointer_type(x.type):
    raise NotImplementedError(f"unsupported type: {x.type}")
  return _sub(_zeros_like(x), x)

