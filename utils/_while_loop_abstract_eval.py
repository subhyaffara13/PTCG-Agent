
def _while_loop_abstract_eval(*avals, cond_jaxpr, body_jaxpr, body_nconsts,
                              cond_nconsts):
  cond_consts_avals, body_consts_avals, in_avals = \
      util.split_list(avals, [cond_nconsts, body_nconsts])

  if len(cond_jaxpr.in_avals) != len(cond_consts_avals) + len(in_avals):
    raise core.JaxprTypeError(
        f"while_loop {len(cond_jaxpr.in_avals)=} but {len(cond_consts_avals) + len(in_avals)=}")
  if len(body_jaxpr.in_avals) != len(body_consts_avals) + len(in_avals):
    raise core.JaxprTypeError(
        f"while_loop {len(body_jaxpr.in_avals)=} but {len(body_consts_avals) + len(in_avals)=}")
  # TODO(mattjj): check body carry type
  # TODO(mattjj): make these typecompat checks work with bints
  # if not all(_map(core.typecompat, [*cond_consts_avals, *in_avals], cond_jaxpr.in_avals)):
  #   cond_avals = [*cond_consts_avals, *in_avals]
  #   a1, a2 = next((a1, a2) for a1, a2 in zip(cond_avals, cond_jaxpr.in_avals)
  #                 if not core.typecompat(a1, a2))
  #   raise core.JaxprTypeError(f"while_loop cond function input type error: {a1} != {a2}")
  # if not all(_map(core.typecompat, [*body_consts_avals, *in_avals], body_jaxpr.in_avals)):
  #   body_avals = [*body_consts_avals, *in_avals]
  #   a1, a2 = next((a1, a2) for a1, a2 in zip(body_avals, body_jaxpr.in_avals)
  #                 if not core.typecompat(a1, a2))
  #   raise core.JaxprTypeError(f"while_loop body function input type error: {a1} != {a2}")


  joined_effects = _join_while_effects(body_jaxpr, cond_jaxpr, body_nconsts,
                                       cond_nconsts)
  disallowed_effects = effects.control_flow_allowed_effects.filter_not_in(joined_effects)
  if disallowed_effects:
    raise NotImplementedError(
        f'Effects not supported in `while`: {disallowed_effects}')
  return body_jaxpr.out_avals, joined_effects

