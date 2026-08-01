
def batch(iterable: cabc.Iterable[V], batch_size: int) -> list[tuple[V, ...]]:
    return list(zip(*repeat(iter(iterable), batch_size), strict=False))


def batch(dataset, batch_size: int):
  """Creates a batched dataset from a one-at-a-time dataset."""
  observations = np.zeros([batch_size] + GAME.observation_tensor_shape(),
                          np.float32)
  labels = np.zeros(batch_size, dtype=np.int32)
  while True:
    for batch_index in range(batch_size):
      observations[batch_index], labels[batch_index] = next(dataset)
    yield observations, labels


def batch(dataset, batch_size: int):
  """Creates a batched dataset from a one-at-a-time dataset."""
  observations = np.zeros([batch_size] + GAME.information_state_tensor_shape(),
                          np.float32)
  labels = np.zeros(batch_size, dtype=np.int32)
  while True:
    for batch_index in range(batch_size):
      observations[batch_index], labels[batch_index] = next(dataset)
    yield observations, labels


def batch(fun: lu.WrappedFun, axis_data,
          in_dims, out_dim_dests, sum_match=False) -> lu.WrappedFun:
  # we split up _batch_inner and _batch_outer for the leak checker
  f = _batch_inner(fun, axis_data, out_dim_dests, sum_match)
  return _batch_outer(f, axis_data, in_dims)

