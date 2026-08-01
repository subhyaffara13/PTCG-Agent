
def int_tuple_from_slice(s: slice) -> tuple[int, ...]:
  """Represents a slice as a tuple of integers."""
  start, stop, step = s.start, s.stop, s.step
  step = step or 1
  try:
    return (int(start), int(stop), int(step))
  except:
    raise ValueError(f'Slice {s} is not concrete.') from None

