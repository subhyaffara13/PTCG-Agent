
def _shard_map_batch(
    trace: batching.BatchTrace, prim: core.Primitive, fun: Callable,
    in_tracers: Sequence[batching.BatchTracer], mesh: Mesh,
    in_specs, check_vma: bool, newly_manual_axes: frozenset,
    debug_info) -> Sequence[batching.BatchTracer]:
  in_vals, in_dims = unzip2(map(trace.to_batch_info, in_tracers))
  spmd_axis_name = trace.axis_data.spmd_name
  explicit_mesh_axis = trace.axis_data.explicit_mesh_axis
  if spmd_axis_name is not None:
    used = {n for spec in in_specs for n in used_axis_names(spec)}
    if not config.disable_vmap_shmap_error.value and set(spmd_axis_name) & used:
      raise ValueError("vmap spmd_axis_name cannot appear in shard_map in_specs")
    new_in_specs = [
        sp if d is None else pxla.batch_spec(sp, d, spmd_axis_name)
        for sp, d in zip(in_specs, in_dims)]
    new_size = trace.axis_data.size // prod(mesh.shape[n] for n in spmd_axis_name)
    new_axis_data = batching.AxisData(
        trace.axis_data.name, new_size, trace.axis_data.spmd_name,
        trace.axis_data.explicit_mesh_axis)
  elif explicit_mesh_axis is not None:
    used = {n for spec in in_specs for n in used_axis_names(spec)}
    if set(explicit_mesh_axis) & used:
      raise ValueError("vmapped away explicit mesh axis cannot appear in "
                       "shard_map in_specs")
    new_in_specs = [
        sp if d is None else pxla.batch_spec(sp, d, None)
        for sp, d in zip(in_specs, in_dims)]
    new_axis_data = trace.axis_data
  else:
    new_in_specs = [sp if d is None else pxla.batch_spec(sp, d, None)
                    for sp, d in zip(in_specs, in_dims)]
    new_axis_data = trace.axis_data

  def fun_batched(*args):
    ans_aux, out_dims = batching.batch_subtrace_2(
        fun, trace.tag, new_axis_data, tuple(in_dims), args)
    ans, out_specs = ans_aux.unpack_aux()
    new_out_specs = _batch_out_specs(spmd_axis_name, explicit_mesh_axis,
                                     out_dims, out_specs)
    return ans.with_aux(out_dims).with_aux(tuple(new_out_specs))

  new_params = dict(mesh=mesh, in_specs=new_in_specs, check_vma=check_vma,
                    newly_manual_axes=newly_manual_axes, debug_info=debug_info)
  # TODO(yashkatariya): Remove remove_explicit_mesh_axis_names when vmap
  # mesh ctx is correctly set.
  with (core.set_current_trace(trace.parent_trace),
        core.remove_explicit_mesh_axis_names(trace.axis_data.explicit_mesh_axis)):
    out_vals = prim.bind(*in_vals, subfuns=(fun_batched,), **new_params)
  make_tracer = partial(batching.BatchTracer, trace,
                        source_info=source_info_util.current())
  out_vals, out_dims = out_vals.unpack_aux()
  return out_vals.map2(make_tracer, out_dims)

