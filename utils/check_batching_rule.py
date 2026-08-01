
def check_batching_rule(batched_args, batch_dims, *, err_tree, debug):
  size = next(x.shape[dim] for x, dim in zip(batched_args, batch_dims)
              if dim is not None)
  batched_args = (batching.bdim_at_front(a, d, size)
                  for a, d in zip(batched_args, batch_dims))
  err = tree_unflatten(err_tree, batched_args)
  _check_error(err, debug=debug)
  return [], []

