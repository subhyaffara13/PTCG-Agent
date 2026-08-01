
def _reshard_transient_array(
    global_transient_array: jax.Array,
    target_sharding: jax.sharding.Sharding | None,
    global_mesh: jax.sharding.Mesh,
) -> jax.Array:
  """Reduces the transient array and reshards to the target sharding."""
  if target_sharding is not None:
    out_sharding = target_sharding
  else:
    out_sharding = jax.sharding.NamedSharding(
        global_mesh, jax.sharding.PartitionSpec()
    )

  return jax.jit(
      lambda x: jnp.sum(x, axis=0).astype(x.dtype), out_shardings=out_sharding
  )(global_transient_array)

