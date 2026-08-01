
def flatten_ir_values(xs: Iterable[IrValues]) -> list[ir.Value]:
  warnings.warn(
      "jax.interpreters.mlir.flatten_ir_values is deprecated. "
      "Use mlir.ir_tree_registry.flatten instead.",
      DeprecationWarning,
      stacklevel=2,
  )
  flat, _ = ir_tree_registry.flatten(xs)
  return flat

