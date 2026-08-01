
def _canonicalize_axis_sizes(axis_sizes: Sequence[int]
                             ) -> tuple[int, ...] | None:
  new_sizes = []
  for s in axis_sizes:
    try:
      new_sizes.append(int(s))
    except:
      return None
  return tuple(new_sizes)

