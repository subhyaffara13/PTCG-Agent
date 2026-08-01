
def primal_sharding_to_cotangent_sharding(sharding):
  return sharding.update(spec=sharding.spec.to_ct_spec())

