
def order_wrt_mesh(mesh, x):
  return tuple(a for a in mesh.axis_names if a in x)

