
def _explicit_axes(fun, *, axes, in_sharding):
  @wraps(fun)
  def decorator(*args, **kwargs):
    if in_sharding is None:
      if "in_sharding" in kwargs:
        _in_sharding = kwargs.pop("in_sharding")
      else:
        raise TypeError("Missing required keyword argument: 'in_sharding'")
    else:
      _in_sharding = in_sharding
    mesh_info = _get_new_mesh(axes, mesh_lib.AxisType.Explicit, 'explicit_axes')
    if mesh_info is None:
      raise ValueError(
          'Context mesh cannot be empty. Please use `jax.set_mesh` API to enter'
          ' into a mesh context when using `explicit_axes` API.')
    with mesh_lib.use_abstract_mesh(mesh_info.new):
      args = reshard(args, _in_sharding)
      out = fun(*args, **kwargs)
    out_specs = tree_map(lambda o: core.modify_spec_for_auto_manual(
        core.typeof(o).sharding.spec, mesh_lib.get_abstract_mesh()), out)
    return reshard(out, out_specs)
  return decorator

