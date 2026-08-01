
def _lu_pivots_body_fn(i, permutation_and_swaps):
  permutation, swaps = permutation_and_swaps
  batch_dims = swaps.shape[:-1]
  fn = _lu_pivots_body_fn_inner
  for _ in range(len(batch_dims)):
    fn = api.vmap(fn, in_axes=(None, 0, 0), out_axes=0)
  return fn(i, permutation, swaps), swaps

