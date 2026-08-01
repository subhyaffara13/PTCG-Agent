
def transform_tree_shardings(input_tree: PyTree) -> Any:
  """Converts shardings/specs/restore-args/arrays to colocated CPU devices."""

  def _transform_leaf_sharding(leaf: Any) -> Any:
    if isinstance(leaf, jax.sharding.Sharding):
      return colocated_cpu_sharding(leaf)
    if isinstance(leaf, jax.ShapeDtypeStruct) and hasattr(leaf, 'sharding'):
      cpu_sharding = colocated_cpu_sharding(leaf.sharding)
      return jax.ShapeDtypeStruct(
          leaf.shape, leaf.dtype, sharding=cpu_sharding
      )
    if isinstance(leaf, jax_array_restore_args.SingleReplicaArrayRestoreArgs):
      return convert_single_replica_restore_args(leaf)
    if isinstance(leaf, jax_array_restore_args.ArrayRestoreArgs):
      return convert_array_restore_args(leaf)
    if isinstance(leaf, jax.Array):
      return to_colocated_python(leaf)
    return leaf

  return jax.tree.map(_transform_leaf_sharding, input_tree)

