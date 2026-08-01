
def unflatten_ir_values_like_types(
    xs: Iterable[ir.Value], ys: Sequence[IrTypes]
) -> list[IrValues]:
  warnings.warn(
      "jax.interpreters.mlir.unflatten_ir_values_like_types is deprecated. "
      "Use treedef.unflatten instead.",
      DeprecationWarning,
      stacklevel=2,
  )
  _, treedef = ir_tree_registry.flatten(ys)
  return treedef.unflatten(xs)

