
def _maybe_shard_array(value, args):
  if hasattr(value, 'reshape') and isinstance(args, ArrayRestoreArgs):
    value = value.reshape(args.global_shape)
    sharding = args.sharding or jax.sharding.NamedSharding(
        args.mesh, args.mesh_axes
    )
    value = jax.make_array_from_callback(
        value.shape, sharding, lambda idx: value[idx]
    )
  return value

