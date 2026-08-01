
def _maybe_modify_sharding(sharding, ndim):
  if len(sharding.spec) == 0 or all(s is None for s in sharding.spec.partitions):
    out = sharding
  elif sharding.mesh.are_all_axes_explicit:
    out = sharding
  else:
    out = sharding.update(spec=modify_spec_for_auto_manual(
        sharding.spec, sharding.mesh))
  if config.remove_size_one_mesh_axis_from_type.value:
    out = out.update(spec=ns.remove_size_one_mesh_axis(out.spec, out.mesh))
  if len(out.spec) != ndim:
    out = _make_lengths_same(out, ndim)
  return out

