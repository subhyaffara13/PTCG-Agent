
def _one_vjp(x):
  x_aval = core.typeof(x)
  ct_s = core.primal_sharding_to_cotangent_sharding(x_aval.sharding)
  ct_s = ct_s.update(spec=ct_s.spec.update(partitions=()))
  return full_like(x, shape=(), fill_value=1, sharding=ct_s)

