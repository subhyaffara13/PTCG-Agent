
def _mpmd_map_partial_eval_custom(saveable, unks_in, inst_in, eqn):
  new_inst = [
      x
      for x, inst in zip(eqn.invars, inst_in)
      if type(x) is jax_core.Var and not inst
  ]
  num_outs = len(eqn.outvars)

  if not unks_in or any(unks_in):
    return None, eqn, [True] * num_outs, [True] * num_outs, new_inst

  if any(isinstance(v.aval, state.AbstractRef) for v in eqn.invars):
    # Force ``mpmd_map`` to run in both forward and backward passes.
    # Otherwise, partial eval only places the ``mpmd_map`` in the forward
    # pass, leaving the backward pass to read newly-allocated but *unchanged*
    # refs.
    return eqn, eqn, [False] * num_outs, [True] * num_outs, new_inst

  policy = pe.ensure_enum(
      saveable(eqn.primitive, *[x.aval for x in eqn.invars], **eqn.params)
  )
  if isinstance(policy, pe.RecomputeType):
    return eqn, eqn, [False] * num_outs, [True] * num_outs, new_inst
  else:
    return eqn, None, [False] * num_outs, [False] * num_outs, []

