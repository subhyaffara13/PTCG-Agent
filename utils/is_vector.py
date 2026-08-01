
def is_vector(v: ir.Value) -> bool:
  return isinstance(v.type, ir.VectorType)

