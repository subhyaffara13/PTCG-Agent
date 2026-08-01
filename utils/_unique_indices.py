
def _unique_indices(indices, *, shape, return_inverse=False,
                    return_index=False, return_true_size=False):
  props = _validate_bcoo_indices(indices, shape)
  f = partial(_unique_indices_unbatched, shape=shape[props.n_batch:],
              return_inverse=return_inverse, return_index=return_index,
              return_true_size=return_true_size)
  f = nfold_vmap(f, props.n_batch, broadcasted=False)
  return f(indices)

