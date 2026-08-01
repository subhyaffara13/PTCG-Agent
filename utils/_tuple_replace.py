
def _tuple_replace(tup, ind, val):
  return tuple(val if i == ind else t for i, t in enumerate(tup))

