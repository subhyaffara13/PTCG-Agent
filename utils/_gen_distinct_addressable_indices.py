
def _gen_distinct_addressable_indices(
    x: np.ndarray | jax.Array | jax.ShapeDtypeStruct,
) -> Generator[Index, None, None]:
  """Yields fragment indices for distinct addressable shards of x."""
  match x:
    case jax.Array() | jax.ShapeDtypeStruct():
      if not x.sharding:
        raise ValueError(
            'Cannot determine addressable shards of jax.ShapeDtypeStruct with'
            ' no sharding.'
        )
      indices = addressable_shards(x)
    case np.ndarray():
      indices = (tuple(slice(0, dim, 1) for dim in x.shape),)
    case _:
      raise TypeError(f'Unsupported type: {type(x)}')
  distinct_indices = sorted({
      *(np_utils.to_hashable_index(i, shape=x.shape) for i in indices)
  })
  yield from (np_utils.from_hashable_index(i) for i in distinct_indices)

