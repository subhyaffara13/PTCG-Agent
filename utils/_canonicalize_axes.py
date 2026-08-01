
def _canonicalize_axes(rank: int, axes: Axes) -> tuple[int, ...]:
  """Returns a tuple of deduplicated, sorted, and positive axes."""
  if not isinstance(axes, Iterable):
    axes = (axes,)
  return tuple({rank + axis if axis < 0 else axis for axis in axes})


def _canonicalize_axes(rank: int, axes: Axes) -> tp.Tuple[int, ...]:
  """Returns a tuple of deduplicated, sorted, and positive axes."""
  if not isinstance(axes, tp.Iterable):
    axes = (axes,)
  return tuple({rank + axis if axis < 0 else axis for axis in axes})


def _canonicalize_axes(rank: int, axes: Axes) -> Sequence[int]:
  """Returns a tuple of deduplicated, sorted, and positive axes."""
  if not isinstance(axes, Iterable):
    axes = (axes,)
  return tuple({rank + axis if axis < 0 else axis for axis in axes})

