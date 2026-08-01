
def _fill_slice(inp_slice: slice, size: int) -> slice:
  assert inp_slice.step is None or inp_slice.step == 1
  start = 0 if inp_slice.start is None else inp_slice.start
  stop = size if inp_slice.stop is None else inp_slice.stop
  assert start >= 0
  assert stop <= size
  return slice(start, stop, None)

