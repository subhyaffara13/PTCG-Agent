
def scalar_result_values(result: jax.Array, *, op_name: str) -> list[Any]:
  """Returns scalar values from workers."""
  values = []
  for shard in result.addressable_shards:
    value = np.asarray(shard.data)
    if value.size != 1:
      raise ValueError(
          f'{op_name}: expected scalar shard value, got shape={value.shape}.'
      )
    values.append(value.item())
  if not values:
    value = np.asarray(result)
    if value.size != 1:
      raise ValueError(
          f'{op_name}: unexpected non-scalar result shape={value.shape}.'
      )
    values.append(value.item())
  return values

