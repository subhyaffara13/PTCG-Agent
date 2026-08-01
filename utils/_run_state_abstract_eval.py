
def _run_state_abstract_eval(*avals: core.AbstractValue, jaxpr: core.Jaxpr,
                             which_linear: tuple[bool, ...],
                             is_initialized: tuple[bool, ...]):
  del which_linear
  assert sum(is_initialized) == len(avals)
  # When we abstractly evaluate `run_state`, we want to keep track of which
  # input avals are `Ref`s and which are not. If an aval is a `Ref`, we want to
  # "propagate" out its inner effects. Otherwise, the effects are local to this
  # `run_state`.
  inner_to_outer_aval_mapping = {}
  outer_ref_index = 0
  for i, is_init in enumerate(is_initialized):
    if not is_init:
      pass
    inner_to_outer_aval_mapping[i] = outer_ref_index
    outer_ref_index += 1
  nonlocal_effects = set()
  is_ref = {i for i, aval in enumerate(avals) if isinstance(aval, AbstractRef)}
  for eff in core.positional_effects(jaxpr):
    if not isinstance(eff, RefEffect):
      nonlocal_effects.add(eff)
      continue
    if eff.input not in inner_to_outer_aval_mapping:
      # This means that this effect corresponds to an uninitialized Ref and
      # should not propagate out of the primitive.
      continue
    # If we do propagate the effect, we need to update the input index to
    # correspond to the outer index.
    outer_index = inner_to_outer_aval_mapping[eff.input]
    if outer_index in is_ref:
      # This means that the effect corresponds to a Ref from an outside scope.
      nonlocal_effects.add(eff.replace(outer_index))
  assert len(jaxpr.invars) == len(is_initialized)
  if not all(is_initialized):
    raise NotImplementedError  # Uninitialized refs are not in avals.
  return avals, nonlocal_effects

