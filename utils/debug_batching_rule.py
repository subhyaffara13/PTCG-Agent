
def debug_batching_rule(args, dims, *, primitive, **params):
  """Unrolls the debug callback across the mapped axis."""
  axis_size = next(x.shape[i] for x, i in zip(args, dims)
                   if i is not None)
  # TODO(sharadmv): implement in terms of rolled loop unstead of unrolled.
  def get_arg_at_dim(i, dim, arg):
    if dim is None:
      # Broadcast unmapped argument
      return arg
    return lax.index_in_dim(arg, i, axis=dim, keepdims=False)
  outs = []
  for i in range(axis_size):
    args_idx = map(partial(get_arg_at_dim, i), dims, args)
    outs.append(primitive.bind(*args_idx, **params))
  outs = [jnp.stack(xs) for xs in zip(*outs)]
  return outs, (0,) * len(outs)

