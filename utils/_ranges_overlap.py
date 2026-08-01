
def _ranges_overlap(
    range1: tuple[slice | int, ...], range2: tuple[slice | int, ...]
) -> bool:
  return all(
      _slices_overlap(r1, r2)
      for r1, r2 in itertools.zip_longest(range1, range2, fillvalue=slice(None))
  )

