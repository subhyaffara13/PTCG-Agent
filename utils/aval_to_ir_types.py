
def aval_to_ir_types(ctx: ModuleContext, aval: core.AbstractValue) -> tuple[ir.Type, ...]:
  """Converts a JAX aval to one or more MLIR IR types.

  In general, a JAX value may be represented by multiple IR values, so this
  function returns a tuple of types. This is the safe version to use when the
  concrete type of ``aval`` is not known.
  """
  ir_types = _aval_to_ir_types(ctx, aval)
  return (ir_types,) if isinstance(ir_types, ir.Type) else ir_types

