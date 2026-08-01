
def add_batched(axis_data, batched_args, batch_dims):
  bdx, bdy = batch_dims
  x, y = batched_args
  if bdx is None and bdy is None:
    return add_jaxvals(x, y), None
  mesh_axis = axis_data.explicit_mesh_axis
  if bdx == bdy:
    return add_jaxvals(x, y), bdx
  elif bdx is None:
    x = broadcast(x, y.shape[bdy], bdy, mesh_axis=mesh_axis)
    return add_jaxvals(x, y), bdy
  elif bdy is None:
    y = broadcast(y, x.shape[bdx], bdx, mesh_axis=mesh_axis)
    return add_jaxvals(x, y), bdx
  else:
    x = moveaxis(x, bdx, bdy)
    return add_jaxvals(x, y), bdy

