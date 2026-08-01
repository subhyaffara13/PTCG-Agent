
def _while_typecheck(_, *in_atoms, cond_jaxpr, body_jaxpr, cond_nconsts,
                     body_nconsts):
  # TODO(frostig,mattjj): check cond_jaxpr, body_jaxpr types
  joined_effects = _join_while_effects(body_jaxpr, cond_jaxpr, body_nconsts,
                                       cond_nconsts)
  disallowed_effects = effects.control_flow_allowed_effects.filter_not_in(joined_effects)
  if disallowed_effects:
    raise NotImplementedError(
        f'Effects not supported in `while`: {disallowed_effects}')
  return body_jaxpr.out_avals, joined_effects

