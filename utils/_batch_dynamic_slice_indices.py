
def _batch_dynamic_slice_indices(indices, bdims):
  if len(indices) == 0:
    return np.array([], 'int32'), None
  empty_marker = object()
  size = next((x.shape[i] for x, i in zip(indices, bdims) if i is not None),
              empty_marker)
  out = next(((typeof(x).sharding.mesh, typeof(x).sharding.spec[i])
              for x, i in zip(indices, bdims) if i is not None), None)
  if size is empty_marker:
    return lax.concatenate([lax.broadcast(i, (1,)) for i in indices], 0), None
  out_s = None if out is None else NamedSharding(out[0], P(out[1], None))
  indices = lax.concatenate(
    [lax.broadcast_in_dim(
        x, (size, 1), broadcast_dimensions=((0,) if i is not None else ()),
        out_sharding=out_s)
     for x, i in zip(indices, bdims)], dimension=1)
  return indices, 0

