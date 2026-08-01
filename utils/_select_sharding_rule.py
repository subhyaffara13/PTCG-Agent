
def _select_sharding_rule(which, *cases):
  non_empty_s = [c.sharding for c in cases if not c.sharding.mesh.empty]
  if not non_empty_s:
    return core.get_cur_mesh_sharding()
  first_s = non_empty_s[0]
  if any(s != first_s for s in non_empty_s[1:]):
    msg = "select cases must have the same shardings, got [{}]."
    raise core.ShardingTypeError(
        msg.format(", ".join([str(c.sharding) for c in cases])))
  # We only check mesh and partitions here (not unreduced/reduced) because
  # select_transpose_rule passes in the primal which to select with cotangent
  # cases. The gradient of which is None anyways.
  eq_p = lambda x, y: x.mesh == y.mesh and x.spec.partitions == y.spec.partitions
  if (which.shape and not which.sharding.mesh.empty and
      not eq_p(which.sharding, first_s)):
    raise core.ShardingTypeError(
        'select `which` must be scalar or have the same sharding as cases, got'
        f' `which` sharding {which.sharding} but case sharding'
        f' {cases[0].sharding}.')
  return first_s

