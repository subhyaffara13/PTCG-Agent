
def _replace_not_ok_with_nan(ctx, batch_dims, ok, x, x_aval):
  num_bcast_dims = len(x_aval.shape) - len(batch_dims)
  select_aval = ShapedArray(batch_dims + (1,) * num_bcast_dims, np.bool_)
  return _broadcasting_select_hlo(
      ctx,
      mlir.broadcast_in_dim(ctx, ok, select_aval,
                            broadcast_dimensions=range(len(batch_dims))),
      select_aval,
      x, x_aval, _nan_like_hlo(ctx, x_aval), x_aval)

