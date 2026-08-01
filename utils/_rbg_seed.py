
def _rbg_seed(seed: typing.Array) -> typing.Array:
  assert not seed.shape
  halfkey = threefry2x32.threefry_seed(seed)
  return jnp.concatenate([halfkey, halfkey])

