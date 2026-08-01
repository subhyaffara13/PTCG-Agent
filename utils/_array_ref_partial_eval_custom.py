
def _array_ref_partial_eval_custom(saveable, unks_in, inst_in, eqn):
  del saveable  # ignored, always full remat array_ref on known input
  unk, = unks_in
  inst, = inst_in
  invar, = eqn.invars
  res = [invar] if not inst else []
  if unk:
    return None, eqn, [True], [True], res  # tangent operation
  else:
    return eqn, eqn, [False], [True], res  # full remat

