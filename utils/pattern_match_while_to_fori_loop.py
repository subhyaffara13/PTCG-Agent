
def pattern_match_while_to_fori_loop(
    cond_jaxpr: jax_core.ClosedJaxpr,
    cond_nconsts: int,
    body_jaxpr: jax_core.ClosedJaxpr,
    body_nconsts: int,
) -> tuple[jax_core.Jaxpr | None, str | None]:
  # Try to pattern match to fori loop.
  # Successful matches produce (jaxpr, None), while failures use the str
  # component of the return tuple to capture information about the failure.
  if cond_nconsts:
    return (None, "Conditional jaxpr can't contain consts.")
  _, cond_invars = split_list(cond_jaxpr.jaxpr.invars, [cond_nconsts])
  cond_in_avals = [v.aval for v in cond_invars]
  if len(cond_in_avals) < 2:
    return (None, "Conditional jaxpr have only two carry args.")
  # Check that the first two carry values are scalar ints
  a1, a2 = cond_in_avals[:2]
  if a1.shape or a1.dtype not in (jnp.int32, jnp.int64):
    return (None, "First conditional jaxpr carry arg is not a scalar int.")
  if a2.shape or a2.dtype not in (jnp.int32, jnp.int64):
    return (None, "Second conditional jaxpr carry arg is not a scalar int.")
  # Check that the only eqn in the cond checks the loop index condition
  v1, v2 = cond_invars[:2]
  outvar = cond_jaxpr.jaxpr.outvars[0]
  assert outvar.aval.dtype == jnp.bool_
  if len(cond_jaxpr.jaxpr.eqns) != 1:
    return (None, "Non-trivial conditional jaxprs not supported.")
  eqn = cond_jaxpr.jaxpr.eqns[0]
  if eqn.primitive != lax.lt_p:
    return (None, "Non-trivial conditional jaxprs not supported.")
  if eqn.outvars != [outvar]:
    return (None, "Non-trivial conditional jaxprs not supported.")
  if eqn.invars != [v1, v2]:
    return (None, "Non-trivial conditional jaxprs not supported.")
  # Check that the carry is updated in the body appropriately
  _, body_invars = split_list(body_jaxpr.jaxpr.invars, [body_nconsts])
  v1, v2 = body_invars[:2]
  vo1, vo2 = body_jaxpr.jaxpr.outvars[:2]
  # Upper bound should be constant
  if v2 is not vo2:
    return (None, "Loop upper bound is not constant.")
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
    return (None, "Loop index not incremented in body.")
  jaxpr = body_jaxpr.jaxpr
  new_invars = (
      *jaxpr.invars[:body_nconsts],
      jaxpr.invars[body_nconsts],
      *jaxpr.invars[body_nconsts + 2 :],
  )
  new_outvars = tuple(jaxpr.outvars[2:])
  if jaxpr.debug_info.arg_names is not None:
    new_arg_names = (*jaxpr.debug_info.arg_names[:body_nconsts],
                     "",
                     *jaxpr.debug_info.arg_names[body_nconsts + 2:])
  else:
    new_arg_names = None
  if jaxpr.debug_info.result_paths is not None:
    new_result_paths = jaxpr.debug_info.result_paths[2:]
  else:
    new_result_paths = None

  jaxpr = jaxpr.replace(
      eqns=jaxpr.eqns[:eqn_index] + jaxpr.eqns[eqn_index + 1 :],
      invars=new_invars,
      outvars=new_outvars,
      debug_info=jaxpr.debug_info._replace(arg_names=new_arg_names,
                                           result_paths=new_result_paths)
  )
  return jaxpr, None

