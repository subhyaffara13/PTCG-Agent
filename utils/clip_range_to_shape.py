
def clip_range_to_shape(
    rnge: tuple[slice | int, ...], shape: tuple[int, ...]
) -> tuple[slice | int, ...] | None:
  """Clips `slice`s in `rnge` to the `shape`. Returns None if `rnge` is entirely out of bounds."""
  result: list[slice | int] = []
  for r, l in zip(rnge, shape, strict=True):
    if isinstance(r, int):
      if r >= l:
        return None
      result.append(r)
    elif isinstance(r, slice):
      if r.start >= l:
        return None
      result.append(slice(r.start, min(r.stop, l), r.step))
    else:
      raise ValueError(f"Unsupported range type: {type(r)}.")
  return tuple(result)

