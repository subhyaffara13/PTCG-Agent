
def reducer_batcher(prim, axis_data, batched_args, batch_dims, axes,
                    **params):
  if all(d is None for d in batch_dims):
    return prim.bind(*batched_args, axes=axes, **params), None
  def out_axis(axes, axis):
    return int(list(np.delete(np.arange(operand.ndim), axes)).index(axis))
  operand, = batched_args
  bdim, = batch_dims
  if isinstance(bdim, int):
    axes = tuple(np.where(np.less(axes, bdim), axes, np.add(axes, 1)))
    bdim_out = out_axis(axes, bdim)
    if 'input_shape' in params:
      params = dict(params, input_shape=operand.shape)
    if 'out_sharding' in params:
      out_s = params['out_sharding']
      if out_s is not None:
        params = dict(params,
                      out_sharding=get_sharding_for_vmap(axis_data, out_s, bdim_out))
    return prim.bind(operand, axes=axes, **params), bdim_out
  else:
    assert False

