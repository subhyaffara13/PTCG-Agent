
def tile_second_to_last_dim(a: jax.typing.ArrayLike) -> jax.Array:
  ones = jnp.ones_like(a)
  a = jnp.expand_dims(a, axis=-1)
  return jnp.expand_dims(ones, axis=-2) * a

