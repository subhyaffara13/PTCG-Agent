
def _prepare_restore_target_shardings(
    state_restore_args: args_lib.PyTreeRestore,
) -> PyTree:
  """Resolves target shardings for restore."""

  def _resolve_restore_arg_sharding(ra: Any) -> jax.sharding.Sharding:
    if not isinstance(ra, type_handlers.ArrayRestoreArgs):
      raise TypeError(
          'Colocated restore requires all restore_args leaves to be '
          f'ArrayRestoreArgs, got {type(ra).__name__}.'
      )
    sharding = ra.sharding
    if isinstance(sharding, sharding_metadata.ShardingMetadata):
      sharding = sharding.to_jax_sharding()
    elif sharding is None and ra.mesh is not None and ra.mesh_axes is not None:
      sharding = jax.sharding.NamedSharding(ra.mesh, ra.mesh_axes)
    if not isinstance(sharding, jax.sharding.Sharding):
      raise ValueError(
          'ArrayRestoreArgs sharding must be a jax.sharding.Sharding, '
          f'got {type(sharding).__name__}.'
      )
    return sharding

  def _resolve_item_sharding(leaf: Any) -> jax.sharding.Sharding:
    sharding = getattr(leaf, 'sharding', None)
    if sharding is None:
      raise ValueError(
          'Colocated restore requires item leaves to provide sharding when '
          f'restore_args is not provided. Got: {leaf!r}'
      )
    if isinstance(sharding, sharding_metadata.ShardingMetadata):
      sharding = sharding.to_jax_sharding()
    if not isinstance(sharding, jax.sharding.Sharding):
      raise ValueError(
          'PyTreeRestore.item sharding must be a jax.sharding.Sharding, '
          f'got {type(sharding).__name__}.'
      )
    return sharding

  if state_restore_args.restore_args is not None:
    return jax.tree.map(
        _resolve_restore_arg_sharding, state_restore_args.restore_args
    )
  return jax.tree.map(_resolve_item_sharding, state_restore_args.item)

