
def _process_event(event):
  """Parse TensorBoard scalars into a (tag, wall_time, step, scalar) tuple."""
  for value in event.summary.value:
    if not _is_scalar_value(value):
      continue

    if value.HasField('tensor'):
      yield (
        value.tag,
        event.wall_time,
        event.step,
        tensor_util.make_ndarray(value.tensor).item(),
      )

