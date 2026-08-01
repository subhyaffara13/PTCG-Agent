
def _extract_nodedefs(x, *, nodedefs: deque[graphlib.GraphDef]):
  if isinstance(x, graphlib.GraphDef):
    nodedefs.append(x)
    return x.with_no_outer_index()
  return x

