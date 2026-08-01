
def build_shaped_array(x, batch_dim: bool = False) -> core.ShapedArray:
  """Builds ShapedArray preserving as much information from x as possible."""
  shape = jnp.shape(x)
  sharding = x.aval.sharding if hasattr(x, "aval") else None
  if batch_dim:
    shape = shape[1:]
    if sharding is not None:
      if sharding.spec[0] is not None:
        raise ValueError(
            "Batch dimension in scan `xs` cannot be sharded."
        )
      sharding = sharding.update(
          spec=jax.sharding.PartitionSpec(*sharding.spec[1:]))
  return core.ShapedArray(
      shape=shape,
      dtype=jnp.result_type(x),
      sharding=sharding,
      **{k: getattr(x, k) for k in ["weak_type", "manual_type"]
         if hasattr(x, k)},
  )

