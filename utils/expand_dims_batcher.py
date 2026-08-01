
def expand_dims_batcher(prim, args, dims, **params):
  """A batching rule for primitives that support matching leading batch
  dimensions in all arguments.
  """
  size, = {x.shape[bd] for x, bd in zip(args, dims) if bd is not None}
  args = [bdim_at_front(x, bd, size) for x, bd in zip(args, dims)]
  out = prim.bind(*args, **params)
  return (out, (0,) * len(out)) if prim.multiple_results else (out, 0)

