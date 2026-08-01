
def bdim_at_front(x, bdim, size, mesh_axis=None):
  if bdim is None:
    return broadcast(x, size, 0, mesh_axis=mesh_axis)
  else:
    return moveaxis(x, bdim, 0)

