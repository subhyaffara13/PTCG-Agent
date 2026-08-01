
def _slice_to_chunk_idx(size: int, slc: slice) -> int:
  if slc.stop == slc.start == None:
    return 0
  slice_size = slc.stop - slc.start
  assert slc.start % slice_size == 0
  assert size % slice_size == 0
  return slc.start // slice_size

