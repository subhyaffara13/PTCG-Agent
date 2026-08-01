
def _state_partial_eval_custom(saveable, unks_in, inst_in, eqn):
  del saveable  # ignored, always full remat state ops on known inputs
                # (except for no_grad_no_remat)
  ref_unk, *_ = unks_in
  ref_inst, *inst_in = inst_in
  _, *val_vars = eqn.invars
  assert ref_inst
  res = [v for v, inst in zip(val_vars, inst_in) if not inst]
  if ref_unk:
    return None, eqn, [True], [True], res  # tangent operation
  elif eqn.invars[0].aval.kind == "no_grad_no_remat":
    return eqn, None, [False], [False], res
  else:
    return eqn, eqn, [False], [True], res  # full remat

