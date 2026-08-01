
def _clamp_batch_rule(batched_args, batch_dims, **params):
  min, x, max = batched_args
  min_bdim, x_bdim, max_bdim = batch_dims
  size = next(x.shape[i] for x, i in zip(batched_args, batch_dims)
              if i is not None)

  # avoid transposes and some broadcasts in special cases
  if min_bdim == x_bdim == max_bdim:
    if np.shape(min) == np.shape(x) == np.shape(max):
      return clamp_p.bind(min, x, max), x_bdim
    elif np.ndim(min) == np.ndim(max) == 0:
      return clamp_p.bind(min, x, max), x_bdim
    elif np.ndim(min) == np.ndim(max) == 1:
      min = broadcast_in_dim(min, x.shape, [min_bdim])
      max = broadcast_in_dim(max, x.shape, [max_bdim])
      return clamp_p.bind(min, x, max), x_bdim
  elif np.ndim(min) == 0 and np.ndim(max) == 0 and x_bdim is not None:
    return clamp_p.bind(min, x, max), x_bdim

  min = batching.bdim_at_front(min, min_bdim, size) if np.shape(min) else min
  max = batching.bdim_at_front(max, max_bdim, size) if np.shape(max) else max
  x = batching.bdim_at_front(x, x_bdim, size) if np.shape(x) else x
  if np.ndim(min) == 0 and np.ndim(x) > 0:
    min = broadcast(min, x.shape)
  if np.ndim(max) == 0 and np.ndim(x) > 0:
    max = broadcast(max, x.shape)
  if 0 < np.ndim(min) < np.ndim(x):
    assert np.ndim(min) == 1, np.ndim(min)
    min = broadcast_in_dim(min, x.shape, [0])
  if 0 < np.ndim(max) < np.ndim(x):
    assert np.ndim(max) == 1, np.ndim(max)
    max = broadcast_in_dim(max, x.shape, [0])
  if np.ndim(min) > np.ndim(x):
    assert np.ndim(x) == 0, np.ndim(x)
    x = broadcast(x, min.shape)
  return clamp_p.bind(min, x, max), 0

