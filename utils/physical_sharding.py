
def physical_sharding(aval, sharding: jsharding.Sharding) -> jsharding.Sharding:
  return make_key_array_phys_sharding(aval, sharding)

