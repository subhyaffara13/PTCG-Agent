
def _seed_func(seed: jnp.int32):
  seed_data = jnp.zeros(tpu_key_impl.key_shape, dtype=jnp.int32)
  return (seed_data + seed).astype(jnp.uint32)  # Broadcast the seed.

