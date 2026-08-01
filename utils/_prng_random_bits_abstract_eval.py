
def _prng_random_bits_abstract_eval(*, shape):
  return jax_core.ShapedArray(shape, jnp.dtype("int32"))

