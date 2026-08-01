
def _batch_out_specs(spmd_name, explicit_mesh_axis, dims, out_specs):
  if spmd_name is not None:
    used = {n for spec in out_specs for n in used_axis_names(spec)}
    if not config.disable_vmap_shmap_error.value and set(spmd_name) & used:
      raise ValueError("vmap spmd_axis_name cannot appear in shard_map out_specs")
    return [sp if d is None else pxla.batch_spec(sp, d, spmd_name)
            for sp, d in zip(out_specs, dims)]
  elif explicit_mesh_axis is not None:
    used = {n for spec in out_specs for n in used_axis_names(spec)}
    if set(explicit_mesh_axis) & used:
      raise ValueError("vmapped away explicit mesh axis cannot appear in "
                       "shard_map out_specs")
    return [sp if d is None else pxla.batch_spec(sp, d, None)
            for sp, d in zip(out_specs, dims)]
  else:
    return [sp if d is None else pxla.batch_spec(sp, d, None)
            for sp, d in zip(out_specs, dims)]

