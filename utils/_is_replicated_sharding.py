import logging

def _is_replicated_sharding(sharding: jax.sharding.Sharding) -> bool:
  """Returns True if the sharding is replicated.

  This is to provide a quick check to decide whether to the sharding would
  produce replicated data. For namedsharding, if any axis is not specified in
  the PartitionSpec, it is considered as replicated.  This function doesn't take
  in the array shape into account as the shape isn't know at the point of
  deserialization.

  We can cache results because we typically expect `save` to be called
  repeatedly on the same model (with changing array values).

  Args:
    sharding: The sharding to check.

  Returns:
    True if the sharding is replicated.
  """
  if isinstance(sharding, jax.sharding.NamedSharding):
    pspec = sharding.spec
    pspec_len = len(pspec)
    mesh_len = len(sharding.mesh.axis_names)
    if mesh_len > pspec_len or not pspec or any((i is None for i in pspec)):
      # replica
      return True
    else:
      return False
  elif isinstance(sharding, jax.sharding.SingleDeviceSharding):
    return True
  else:
    logging.warning(
        'Unsupported sharding type, assuming not replicated: %s', sharding
    )
    return False

