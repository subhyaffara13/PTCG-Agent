
def _debug_partial_eval_custom(saveable, unks_in, inst_in, eqn, primitive):
  # The default behavior for effectful primitives is to not stage them if
  # possible. For debug callback, we actually want it to be staged to
  # provide more information to the user. This rule bypasses partial_eval's
  # regular behavior to do that. Specifically, we will stage the callback
  # if:
  # 1) the policy says debug_callbacks are not saveable
  # 2) the policy says debug_callbacks are saveable BUT all of the input
  #    values are instantiated.
  # The purpose is to call back with as much information as possible while
  # avoiding unnecessarily staging out other values.
  if any(unks_in):
    # The usual case (if we have any unknowns, we need to stage it out)
    res = [v for v, inst in zip(eqn.invars, inst_in) if not inst]
    return None, eqn, [], [], res
  if saveable(primitive, *[v.aval for v in eqn.invars], **eqn.params):
    # The policy is telling us we can save the debug callback.
    if all(inst_in):
      # If all of the inputs are instantiated, we also stage out the
      # debug_callback.
      return eqn, eqn, [], [], []
    else:
      # If any are not instantiated, we don't do any extra staging to avoid
      # affecting the computation.
      return eqn, None, [], [], []
  # If we can't save the debug callback (thanks to the policy) we listen to
  # the policy and stage out the debug callback.
  return eqn, eqn, [], [], []

