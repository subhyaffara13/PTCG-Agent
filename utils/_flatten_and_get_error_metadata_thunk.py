
def _flatten_and_get_error_metadata_thunk(f, store, *invals):
  error, out = f(*invals)
  out_vals, out_tree = jtu.tree_flatten((error, out))
  store.store((out_tree, set(error._pred.keys())))
  return out_vals

