
def convert_array_restore_args(
    restore_args: jax_array_restore_args.ArrayRestoreArgs,
) -> jax_array_restore_args.ArrayRestoreArgs:
  """Converts ArrayRestoreArgs to use colocated CPU devices."""
  if restore_args.mesh is not None:
    cpu_mesh = cp.colocated_cpu_devices(restore_args.mesh)
    logging.vlog(
        2,
        'Converting restore mesh with axis names %s to colocated CPU mesh.',
        restore_args.mesh.axis_names,
    )
    restore_args = dataclasses.replace(restore_args, mesh=cpu_mesh)
  if restore_args.sharding is None:
    return restore_args
  if isinstance(restore_args.sharding, jax.sharding.Sharding):
    cpu_sharding = colocated_cpu_sharding(restore_args.sharding)
    logging.vlog(
        2,
        'Converting restore sharding from %s to colocated CPU sharding %s',
        restore_args.sharding,
        cpu_sharding,
    )
    return dataclasses.replace(restore_args, sharding=cpu_sharding)
  if isinstance(restore_args.sharding, sharding_metadata.ShardingMetadata):
    sharding = restore_args.sharding.to_jax_sharding()
    cpu_sharding = colocated_cpu_sharding(sharding)
    logging.vlog(
        2,
        'Converting restore sharding metadata %s to colocated CPU sharding %s',
        type(restore_args.sharding).__name__,
        cpu_sharding,
    )
    return dataclasses.replace(
        restore_args,
        sharding=restore_args.sharding.from_jax_sharding(cpu_sharding),
    )
  raise TypeError(
      f'Sharding type {type(restore_args.sharding)} not supported in'
      ' to_colocated_python.'
  )

