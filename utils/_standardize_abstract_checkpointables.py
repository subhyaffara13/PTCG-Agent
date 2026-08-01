
def _standardize_abstract_checkpointables(abstract_checkpointables):
  """Standardizes abstract checkpointables for loading.

  This function resolves AbstractMesh instances within NamedSharding to concrete
  Mesh instances and extracts metadata if the input is a CheckpointMetadata
  object.

  Args:
    abstract_checkpointables: The abstract checkpointables, potentially wrapped
      in CheckpointMetadata.

  Returns:
    The standardized abstract checkpointables.
  """

  def _resolve_abstract_mesh(leaf):
    if (
        hasattr(leaf, 'sharding')
        and isinstance(leaf.sharding, jax.sharding.NamedSharding)
        and isinstance(leaf.sharding.mesh, jax.sharding.AbstractMesh)
    ):
      new_sharding = jax.sharding.NamedSharding(
          jax.sharding.get_mesh(), leaf.sharding.spec
      )
      return jax.ShapeDtypeStruct(leaf.shape, leaf.dtype, sharding=new_sharding)
    return leaf

  if isinstance(abstract_checkpointables, CheckpointMetadata):
    abstract_checkpointables = abstract_checkpointables.metadata
  elif abstract_checkpointables is not None and hasattr(
      jax.sharding, 'get_mesh'
  ):
    # jax.sharding.get_mesh() was recently added so check to ensure that we
    # don't crash on older versions.
    return jax.tree_util.tree_map(
        _resolve_abstract_mesh, abstract_checkpointables
    )
  return abstract_checkpointables

