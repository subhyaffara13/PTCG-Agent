
def nonzero_tangent_outputs(f, store, *args, **kwargs):
  results = (_, tangents_out) = f(*args, **kwargs)
  store.store([type(r) is not Zero for r in tangents_out])
  return results

