
def array_result_values(result: jax.Array, *, op_name: str) -> list[np.ndarray]:
  """Returns array values from workers."""
  values = []
  for shard in result.addressable_shards:
    values.append(np.asarray(shard.data))
  if not values:
    values.append(np.asarray(result))
  for value in values:
    if value.ndim == 0:
      raise ValueError(f'{op_name}: expected array shard value, got scalar.')
  return values

