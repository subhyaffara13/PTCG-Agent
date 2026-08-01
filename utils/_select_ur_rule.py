
def _select_ur_rule(which, *cases):
  non_empty_cs = [c for c in cases if not c.sharding.mesh.empty]
  if not non_empty_cs:
    return frozenset(), frozenset()
  # which and all cases have the same sharding check is already done in select
  # sharding rule.
  return core.getu(non_empty_cs[0]), core.getr(non_empty_cs[0])

