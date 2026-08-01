
def _raise_to_slice(slc: slice | int):
  if isinstance(slc, int):
    return slice(slc, slc + 1)
  return slc

