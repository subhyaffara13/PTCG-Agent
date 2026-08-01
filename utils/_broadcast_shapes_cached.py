
def _broadcast_shapes_cached(*shapes: tuple[int, ...]) -> tuple[int, ...]:
  return _broadcast_shapes_uncached(*shapes)

