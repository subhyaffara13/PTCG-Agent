
def _make_specs_for_serialized_specs(
    devices: DeviceList,
) -> api.ShapeDtypeStruct:
  """Makes output specs for serialized specs."""
  mesh = jax.sharding.Mesh(tuple(devices), ("x",))
  replicated_sharding = jax.sharding.NamedSharding(
      mesh, jax.sharding.PartitionSpec()
  )
  return api.ShapeDtypeStruct(
      shape=(), dtype=np.dtypes.StringDType(), sharding=replicated_sharding
  )

