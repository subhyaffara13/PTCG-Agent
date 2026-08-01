
def _restore_sharding_from_metadata(
    leaf: Any,
    global_mesh: jax.sharding.Mesh,
) -> jax.sharding.Sharding | None:
  """Builds explicit restore shardings from checkpoint metadata.

  When callers use bare `PyTreeRestore()`, Orbax falls back to reading per-leaf
  sharding files at restore time. Reconstructing restore shardings once from the
  already-loaded tree metadata keeps restore on the standard backend path while
  avoiding that slower and less explicit fallback.

  Named shardings are rebuilt against the live global mesh using the saved
  partition spec. Single-device shardings are rebuilt from the exact saved
  device string because those leaves are not mesh-relative.

  Args:
    leaf: The array metadata leaf.
    global_mesh: The global JAX device mesh.

  Returns:
    The reconstructed sharding, or None if not applicable.
  """
  if not isinstance(leaf, value_metadata.ArrayMetadata):
    return None
  if leaf.sharding is None:
    raise ValueError(
        'ArrayMetadata for restore must include sharding metadata.'
    )

  if isinstance(leaf.sharding, sharding_metadata.NamedShardingMetadata):
    return jax.sharding.NamedSharding(
        global_mesh,
        jax.sharding.PartitionSpec(*leaf.sharding.partition_spec),
    )
  if isinstance(leaf.sharding, sharding_metadata.SingleDeviceShardingMetadata):
    # Single-device metadata already carries the exact local device string that
    # saved the leaf. Reconstruct that specific device instead of collapsing all
    # such leaves onto global_mesh.devices.flat[0], which would silently change
    # the restore contract for scalar or host-local leaves.
    return leaf.sharding.to_jax_sharding()

  raise ValueError(
      'Unsupported sharding metadata for restore:'
      f' {type(leaf.sharding)}'
  )

