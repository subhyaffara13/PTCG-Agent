
def make_key_array_phys_sharding(aval, sharding):
  if sharding.num_devices == 1:
    return sharding
  elif isinstance(sharding, NamedSharding):
    elt_aval = core.physical_element_aval(aval.dtype)
    trailing_spec = [None] * elt_aval.ndim
    return sharding.update(spec=PartitionSpec(*sharding.spec, *trailing_spec))
  else:
    hlos = sharding._to_xla_hlo_sharding(aval.ndim)
    return GSPMDSharding(
        sharding._internal_device_list, physical_hlo_sharding(aval, hlos))

