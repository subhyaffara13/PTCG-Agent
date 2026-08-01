
def _rng_bit_generator_sharding_rule(key, *, shape, dtype, algorithm,
                                     out_sharding):
  if out_sharding is None:
    out_sharding = core.get_cur_mesh_sharding()
  return (key.sharding, out_sharding)

