
def _concatenate_sharding_rule(*operands, **kwargs):
  non_empty_s = [o.sharding for o in operands if not o.sharding.mesh.empty]
  if not non_empty_s:
    return core.get_cur_mesh_sharding()
  if not all(s == non_empty_s[0] for s in non_empty_s):
    ss = ", ".join(str(o.sharding) for o in operands)
    raise core.ShardingTypeError(
        f"All operands should have the same sharding. Got shardings {ss}")
  return non_empty_s[0]

