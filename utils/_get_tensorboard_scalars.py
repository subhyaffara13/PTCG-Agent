import itertools

def _get_tensorboard_scalars(path):
  """Read and parse scalar TensorBoard summaries.

  Args:
    path: str. Path containing TensorBoard event files.

  Returns:
    Dictionary mapping summary tags (str) to lists of
    (wall_time, step, scalar) tuples.
  """
  gen = _make_events_generator(path)
  data = filter(lambda x: x.HasField('summary'), gen)
  data = itertools.chain.from_iterable(map(_process_event, data))

  data_by_key = {}
  for tag, wall_time, step, value in data:
    if not tag in data_by_key:
      data_by_key[tag] = []
    data_by_key[tag].append((wall_time, step, value))
  return data_by_key

