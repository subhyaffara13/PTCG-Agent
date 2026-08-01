
def flatten_ir_types(xs: Iterable[IrTypes]) -> list[ir.Type]:
  warnings.warn(
      "jax.interpreters.mlir.flatten_ir_types is deprecated. "
      "Use mlir.ir_tree_registry.flatten instead.",
      DeprecationWarning,
      stacklevel=2,
  )
  flat, _ = ir_tree_registry.flatten(xs)
  return flat

