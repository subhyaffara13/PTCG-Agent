
def _core_map_partial_eval_custom(saveable, unks_in, inst_in, eqn):
  assert all(inst_in)
  if all(unks_in):
    return None, eqn, [], [], []  # purely unknown
  elif not any(unks_in):
    return eqn, eqn, [], [], []  # full remat
  else:
    # Some values, e.g. empty refs or refs initialized to constant zero, can be
    # 'known', but really they belong in the staged/tangent computation. We
    # encounter them here as known inputs mixed in with unknown/tangent inputs,
    # which tells us that this core_map is really a purely tangent computation.
    return None, eqn, [], [], []

