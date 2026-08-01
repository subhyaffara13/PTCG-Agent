
def _select_and_gather_add_batching_rule(
    batched_args, batch_dims, *, select_prim, window_dimensions, window_strides,
    padding, base_dilation, window_dilation):
  t, x = batched_args
  t_bdim, x_bdim = batch_dims
  size = next(a.shape[bdim] for a, bdim in zip(batched_args, batch_dims)
              if bdim is not None)
  t = batching.bdim_at_front(t, t_bdim, size)
  x = batching.bdim_at_front(x, x_bdim, size)
  window_dimensions = (1,) + window_dimensions
  window_strides = (1,) + window_strides
  padding = ((0, 0),) + padding
  base_dilation = (1,) + base_dilation
  window_dilation = (1,) + window_dilation
  out = _select_and_gather_add(t, x, select_prim, window_dimensions,
                               window_strides, padding, base_dilation,
                               window_dilation)
  return (out, 0)

