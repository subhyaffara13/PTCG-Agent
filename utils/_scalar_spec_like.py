
def _scalar_spec_like(
    arg_spec: jax.ShapeDtypeStruct, dtype: jnp.dtype
) -> jax.ShapeDtypeStruct:
  return jax.ShapeDtypeStruct((), dtype=dtype, sharding=arg_spec.sharding)

