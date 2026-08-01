
def ir_attribute(val: Any) -> ir.Attribute:
  """Convert a Python value to an MLIR attribute."""
  for t in type(val).__mro__:
    handler = _attribute_handlers.get(t)
    if handler:
      out = handler(val)
      assert isinstance(out, ir.Attribute), (type(val), out)
      return out
  m = getattr(val, '__jax_array__', None)
  if m is not None:
    return ir_attribute(m())
  raise TypeError(f"No attribute handler defined for type: {type(val)}")

