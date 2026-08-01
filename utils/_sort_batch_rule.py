
def _sort_batch_rule(batched_args, batch_dims, *, dimension, is_stable, num_keys):
  prototype_arg, new_bdim = next(
    (a, b) for a, b in zip(batched_args, batch_dims) if b is not None)
  new_args = []
  for arg, bdim in zip(batched_args, batch_dims):
    if bdim is None:
      dims = [int(dim) for dim in np.delete(np.arange(prototype_arg.ndim), new_bdim)]
      new_args.append(broadcast_in_dim(
          arg, prototype_arg.shape, dims,
          out_sharding=typeof(prototype_arg).sharding))
    else:
      new_args.append(batching.moveaxis(arg, bdim, new_bdim))
  new_dimension = dimension + (new_bdim <= dimension)
  bdims = (new_bdim,) * len(new_args)
  return (sort_p.bind(*new_args, dimension=new_dimension, is_stable=is_stable, num_keys=num_keys),
          bdims)

