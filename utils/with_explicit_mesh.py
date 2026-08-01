
def with_explicit_mesh(sizes, names, axis_types=None, iota_order=False):
  axis_types = ((mesh_lib.AxisType.Explicit,) * len(names)
                if axis_types is None else axis_types)
  def decorator(fn):
    def mesh_fn(*args, **kwargs):
      mesh = create_mesh(sizes, names, iota_order, axis_types=axis_types)
      with sharding_impls.set_mesh(mesh):
        return fn(*args, **kwargs, mesh=mesh)
    return mesh_fn
  return decorator

