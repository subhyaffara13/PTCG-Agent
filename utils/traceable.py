
def traceable(f, store, in_tree_def, *primals_and_series):
  primals_in, series_in = tree_unflatten(in_tree_def, primals_and_series)
  primals_out, series_out = f(primals_in, series_in)
  out_flat, out_tree_def = tree_flatten((primals_out, series_out))
  store.store(out_tree_def)
  return out_flat


def traceable(f, store, in_tree, *primals_and_tangents):
  primals, tangents = tree_unflatten(in_tree, primals_and_tangents)
  tangents = [p2tz(p) if t is None else t
              for p, t in zip(primals, tangents)]
  primals_out, tangents_out = f(primals, tangents)
  tangents_out = [None if type(t) is Zero else t for t in tangents_out]
  out_flat, out_tree = tree_flatten((primals_out, tangents_out))
  store.store(out_tree)
  return out_flat

