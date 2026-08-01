
def worker_rank_from_array(rank_array: jax.Array) -> int:
  """Extracts a colocated worker's logical rank from a sharded rank array."""
  addressable_shards = tuple(getattr(rank_array, 'addressable_shards', ()))
  if len(addressable_shards) == 1:
    rank_value = np.asarray(addressable_shards[0].data)
  elif len(addressable_shards) > 1:
    raise ValueError(
        'Expected exactly one addressable logical worker rank shard for this '
        f'colocated worker, got {len(addressable_shards)}.'
    )
  else:
    rank_value = None

  is_fully_addressable = getattr(rank_array, 'is_fully_addressable', True)
  if callable(is_fully_addressable):
    is_fully_addressable = is_fully_addressable()
  if rank_value is None and is_fully_addressable:
    rank_value = np.asarray(rank_array)
  if rank_value is None:
    raise ValueError(
        'Expected exactly one addressable logical worker rank shard for this '
        'colocated worker, got 0.'
    )
  if rank_value.size != 1:
    raise ValueError(
        'Expected exactly one logical worker rank for this colocated worker, '
        f'got shape={rank_value.shape}.'
    )
  return int(rank_value.reshape(-1)[0])

