import functools

def _sparsify_with_interpreter(f):
  """Implementation of sparsify() using jaxpr interpreter."""
  f_raw = sparsify_raw(f)
  @functools.wraps(f)
  def wrapped(*args, **params):
    spenv = SparsifyEnv()
    spvalues = arrays_to_spvalues(spenv, args)
    spvalues_out, out_tree = f_raw(spenv, *spvalues, **params)
    out = spvalues_to_arrays(spenv, spvalues_out)
    return tree_unflatten(out_tree, out)
  return wrapped

