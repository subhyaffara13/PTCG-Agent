
def _auto_axes(fun, *, axes_, out_sharding):
  @wraps(fun)
  def decorator(*args, **kwargs):
    if out_sharding is None:
      if "out_sharding" in kwargs:
        _out_sharding = kwargs.pop("out_sharding")
      else:
        raise TypeError("Missing required keyword argument: 'out_sharding'")
    else:
      _out_sharding = out_sharding
    mesh_info = _get_new_mesh(
        axes_, mesh_lib.AxisType.Auto, 'auto_axes', shardings=_out_sharding)
    if mesh_info is None:
      return fun(*args, **kwargs)
    if set(mesh_info.prev.auto_axes) == set(mesh_info.axes):
      return fun(*args, **kwargs)
    with mesh_lib.use_abstract_mesh(mesh_info.new):
      in_specs = tree_map(lambda a: core.modify_spec_for_auto_manual(
          core.typeof(a).sharding.spec, mesh_info.new), args)
      args = reshard(args, in_specs)
      out = fun(*args, **kwargs)
    return reshard(out, _out_sharding)
  return decorator

