
def strip_trailing_nones(lst):
  while lst[-1] is None:
    lst.pop()
  return tuple(lst)

