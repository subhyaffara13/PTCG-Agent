
def strip_sharding_metadata(tree: Any) -> Any:
  """Strips concrete sharding_metadata from Metadata to decouple from topologies."""
  def _strip(x):
    # Check for sharding_metadata attribute since it may reach leaves that are
    # not arrays.
    if hasattr(x, 'sharding_metadata'):
      return array_leaf_handler.ArrayMetadata(
          shape=x.shape,
          dtype=x.dtype,
          sharding_metadata=None,
          storage_metadata=x.storage_metadata,
      )
  return jax.tree.map(
      _strip,
      tree,
      is_leaf=lambda leaf: hasattr(leaf, 'sharding_metadata'),
  )

