
def _addupdate_partial_eval_custom(saveable, unks_in, inst_in, eqn):
  del saveable  # ignored, always full remat state ops on known inputs
  ref_unk, *_ = unks_in
  ref_inst, *inst_in = inst_in
  _, *val_vars = eqn.invars
  assert ref_inst
  res = [v for v, inst in zip(val_vars, inst_in) if not inst]
  if ref_unk:
    return None, eqn, [], [], res  # tangent operation
  else:
    return eqn, eqn, [], [], res  # full remat

