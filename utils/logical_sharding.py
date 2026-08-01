
def logical_sharding(logical_shape, dtype, phys_sharding) -> jsharding.Sharding:
  # The trailing dims should always be replicated.
  # TODO(yashkatariya): Maybe remove this check or do this at the pxla level?
  check_replicated_trailing_dims(phys_sharding, logical_shape, dtype)

  if phys_sharding.num_devices == 1:
    return phys_sharding
  elif isinstance(phys_sharding, NamedSharding):
    elt_aval = core.physical_element_aval(dtype)
    phys_shape = core.physical_shape(logical_shape, dtype)
    if len(phys_sharding.spec) < len(phys_shape):
      phys_spec = (*phys_sharding.spec,
                   *[None] * (len(phys_shape) - len(phys_sharding.spec)))
    else:
      phys_spec = phys_sharding.spec
    return phys_sharding.update(spec=phys_spec[:-elt_aval.ndim])
  else:
    return get_logical_gspmd_sharding(logical_shape, dtype, phys_sharding)

