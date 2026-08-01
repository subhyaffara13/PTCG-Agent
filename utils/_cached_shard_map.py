
def _cached_shard_map(fun, in_tree, in_axes_flat, out_axes_flat, out_axes_tree,
                      donated_invars, mesh_devices, axis_name):
  mesh = Mesh(mesh_devices, (axis_name,))
  out_axes = tree_unflatten(out_axes_tree, list(out_axes_flat))
  in_specs = tuple(map(partial(_axes_to_pspec, axis_name), in_axes_flat))
  out_specs = tree_map(
      partial(_axes_to_pspec, axis_name), out_axes, is_leaf=lambda x: x is None
  )
  def _fun(*flat_args):
    args = tree_map(
        lambda x, ax: x if ax is None else lax.squeeze(x, [ax]),
        flat_args,
        in_axes_flat,
    )
    args, kwargs = tree_unflatten(in_tree, args)
    out = fun.call_wrapped(*args, **kwargs)
    out_flat, out_tree = tree_flatten(out)
    out_axes_flat = broadcast_prefix(out_axes, out, is_leaf=lambda x: x is None)
    out_flat = tree_map(
        lambda x, ax: x if ax is None else lax.expand_dims(x, [ax]),
        out_flat,
        out_axes_flat,
    )
    return tree_unflatten(out_tree, out_flat)
  _pmapped = shard_map(_fun, mesh=mesh, in_specs=in_specs, out_specs=out_specs,
                       check_vma=False, axis_names=set(mesh.axis_names))
  # Donation is now safe in multi-host mode because host_local_array_to_global_array
  # copies donated arrays instead of rewrapping them (which would share buffers).
  donate_argnums = [i for i, val in enumerate(donated_invars) if val]

  # out_specs is a pytree, so use tree_map to convert to shardings
  get_sharding = (
      lambda spec: sharding_impls.NamedSharding(mesh, spec)
      if spec is not None else spec)
  out_global_shardings = tree_map(
      get_sharding, out_specs, is_leaf=lambda x: x is None)

  @util.cache()
  def out_local_shardings_thunk(pspec):
    return (
        sharding_impls.NamedSharding(mesh.local_mesh, pspec),
        sharding_impls.NamedSharding(mesh, pspec),
    )

  local_devices = list(mesh.local_mesh.devices.flat)
  in_local_shardings = [
      sharding_impls.NamedSharding(mesh.local_mesh, p) for p in in_specs]
  in_global_shardings = [
      sharding_impls.NamedSharding(mesh, p) for p in in_specs]
  jitted_f = api.jit(_pmapped, donate_argnums=donate_argnums)
  jitted_f_with_shardings = api.jit(
      _pmapped,
      donate_argnums=donate_argnums,
      in_shardings=tuple(in_global_shardings),
      out_shardings=out_global_shardings,
  )
  return CachedShardMap(
      pmapped=_pmapped,
      in_specs_flat=in_specs,
      local_devices=local_devices,
      in_local_shardings=in_local_shardings,
      in_global_shardings=in_global_shardings,
      mesh=mesh,
      out_specs=out_specs,
      out_local_shardings_thunk=out_local_shardings_thunk,
      donate_argnums=donate_argnums,
      out_global_shardings=out_global_shardings,
      jitted_f=jitted_f,
      jitted_f_with_shardings=jitted_f_with_shardings,
  )

