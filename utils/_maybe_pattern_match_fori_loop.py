
def _maybe_pattern_match_fori_loop(
    ctx: LoweringRuleContext,
    *args,
    cond_nconsts,
    cond_jaxpr,
    body_nconsts,
    body_jaxpr,
):
  if cond_nconsts:
    return None
  _, cond_invars = split_list(cond_jaxpr.jaxpr.invars, [cond_nconsts])
  cond_in_avals = [v.aval for v in cond_invars]
  if len(cond_in_avals) < 2:
    return None
  # Check that the first two carry values are scalar ints
  a1, a2 = cond_in_avals[:2]
  if a1.shape != () or a1.dtype not in (jnp.int32, jnp.int64):
    return None
  if a2.shape != () or a2.dtype not in (jnp.int32, jnp.int64):
    return None
  # Check that the only eqn in the cond checks the loop index condition
  v1, v2 = cond_invars[:2]
  outvar = cond_jaxpr.jaxpr.outvars[0]
  assert outvar.aval.dtype == jnp.bool_
  if len(cond_jaxpr.jaxpr.eqns) != 1:
    return None
  eqn = cond_jaxpr.jaxpr.eqns[0]
  if eqn.primitive != lax.lt_p:
    return None
  if eqn.outvars != [outvar]:
    return None
  if eqn.invars != [v1, v2]:
    return None
  # Check that the carry is updated in the body appropriately
  _, body_invars = split_list(body_jaxpr.jaxpr.invars, [body_nconsts])
  v1, v2 = body_invars[:2]
  vo1, vo2 = body_jaxpr.jaxpr.outvars[:2]
  # Upper bound should be constant
  if v2 is not vo2:
    return None
  # Check that we increment the loop index in the body
  for i, eqn in enumerate(body_jaxpr.jaxpr.eqns):
    if eqn.primitive is lax.add_p:
      if eqn.invars[0] is v1:
        if isinstance(eqn.invars[1], jax_core.Literal):
          if eqn.invars[1].val == 1:
            if eqn.outvars[0] == vo1:
              eqn_index = i
              break
  else:
    return None
  jaxpr = body_jaxpr.jaxpr
  new_invars = (*jaxpr.invars[:body_nconsts],
                jaxpr.invars[body_nconsts],
                *jaxpr.invars[body_nconsts + 2:])
  new_outvars = tuple(jaxpr.outvars[2:])
  jaxpr = jaxpr.replace(
      eqns=jaxpr.eqns[:eqn_index] + jaxpr.eqns[eqn_index + 1:],
      invars=new_invars,
      outvars=new_outvars,
      debug_info=jaxpr.debug_info.with_unknown_names())
  _, body_consts, carry = split_list(args, [cond_nconsts, body_nconsts])
  (lb, ub), args = carry[:2], carry[2:]
  const_block_infos, args_block_infos = split_list(ctx.block_infos,
                                                   [body_nconsts])
  ctx = ctx.replace(block_infos=[*const_block_infos, None,
                                 *args_block_infos[2:]])
  for_out = _lower_jaxpr_to_for_loop(
      ctx,
      jaxpr,
      lb,
      ub,
      body_consts,
      *args,
      has_loop_index=True,
      step=1,
      bound_type=lb.type,
  )
  return [ub, ub, *for_out]

