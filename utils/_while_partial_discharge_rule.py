
def _while_partial_discharge_rule(should_discharge, in_avals, out_avals, *args,
    cond_jaxpr, body_jaxpr, cond_nconsts, body_nconsts):
  del out_avals
  cond_consts_discharge, body_consts_discharge, carry_discharge = split_list(
      should_discharge, [cond_nconsts, body_nconsts])
  cond_consts, body_consts, carry = split_list(args, [cond_nconsts, body_nconsts])
  cond_consts_avals, body_consts_avals, carry_avals = split_list(in_avals,
                                                                 [cond_nconsts,
                                                                  body_nconsts])

  # Check if the same Ref is written to in both cond and body.
  cond_write_ids = {id(cond_consts_avals[effect.input])
    for effect in core.positional_effects(cond_jaxpr)
    if isinstance(effect, state.WriteEffect)}
  cond_has_writes = len(cond_write_ids) > 0
  body_write_ids = {id(body_consts_avals[effect.input])
    for effect in core.positional_effects(body_jaxpr)
    if isinstance(effect, state.WriteEffect)}
  write_to_both_ids = cond_write_ids & body_write_ids
  if write_to_both_ids:
    raise NotImplementedError(
        "Cannot write to the same ref in both cond and body of while loop.")

  cond_is_ref = [
      isinstance(aval, state.AbstractRef) and should
      for aval, should in zip(cond_consts_avals, cond_consts_discharge)
  ]
  remaining_cond_consts, cond_refs = partition_list(cond_is_ref, cond_consts)
  remaining_cond_const_avals, cond_ref_avals = partition_list(cond_is_ref,
                                                         cond_consts_avals)
  num_cond_refs = sum(cond_is_ref)
  num_remaining_cond_consts = cond_nconsts - num_cond_refs
  body_is_ref = [
      isinstance(aval, state.AbstractRef) and should
      for aval, should in zip(body_consts_avals, body_consts_discharge)
  ]
  remaining_body_consts, body_refs = partition_list(body_is_ref, body_consts)
  remaining_body_const_avals, body_ref_avals = partition_list(body_is_ref,
                                                         body_consts_avals)
  num_body_refs = sum(body_is_ref)
  num_remaining_body_consts = body_nconsts - num_body_refs
  num_out_body_consts = num_remaining_body_consts
  if cond_has_writes:
    # If the cond has writes, we need to add the cond consts into the body
    # consts since we need to evaluate the cond condition in the body.
    remaining_body_consts = [*remaining_cond_consts, *remaining_body_consts]
    remaining_body_const_avals = [*remaining_cond_const_avals,
                                  *remaining_body_const_avals]
    num_remaining_body_consts += num_remaining_cond_consts

  num_carry = len(in_avals) - body_nconsts - cond_nconsts
  if body_jaxpr.consts:
    raise NotImplementedError("Body jaxpr has consts. If you see this error, "
                              "please open an issue at "
                              "https://github.com/jax-ml/jax/issues")
  if cond_jaxpr.consts:
    raise NotImplementedError("Cond jaxpr has consts. If you see this error, "
                              "please open an issue at "
                              "https://github.com/jax-ml/jax/issues")
  discharged_cond_jaxpr = state_discharge.discharge_state(
      cond_jaxpr, should_discharge=[*cond_consts_discharge, *carry_discharge]
  )
  if discharged_cond_jaxpr.consts:
    raise NotImplementedError
  # body_jaxpr has the signature (*body_consts, *carry) -> carry.
  # Some of these body_consts are actually `Ref`s so when we discharge
  # them, they also turn into outputs, effectively turning those consts into
  # carries. However this doesn't fit the expected signature for the body_jaxpr.
  # Therefore we need to rewrite the jaxpr to shuffle around the `Ref`s so that
  # they are part of the carry.
  discharged_body_jaxpr = state_discharge.discharge_state(
      body_jaxpr, should_discharge=[*body_consts_discharge, *carry_discharge]
  )
  if discharged_body_jaxpr.consts:
    raise NotImplementedError

  def new_body(*consts_refs_carry):
    consts, body_refs, cond_refs, carry = split_list(
        consts_refs_carry,
        [num_remaining_body_consts, num_body_refs, num_cond_refs])
    if cond_has_writes:
      # We run the cond jaxpr in the body so that Refs that are updated
      # in the cond jaxpr are persisted via the carry.
      cond_consts, body_consts = split_list(consts, [num_remaining_cond_consts])
      cond_consts_and_refs = merge_lists(cond_is_ref, cond_consts, cond_refs)
      cond_carry_refs = core.eval_jaxpr(
          discharged_cond_jaxpr.jaxpr,
          discharged_cond_jaxpr.consts,
          *cond_consts_and_refs,
          *carry,
      )
      # Note: in order to handle the same Ref being updated in both the cond
      # and body, we would need to interleave the updated cond_carry_refs into
      # body_refs here.
      # Currently we disallow this so we don't need to handle it.
      _, cond_refs_out = split_list(cond_carry_refs, [1])
      assert len(cond_refs_out) == len(cond_refs)
    else:
      body_consts = consts
      cond_refs_out = cond_refs

    body_consts_and_refs = merge_lists(body_is_ref, body_consts, body_refs)
    body_carry_refs = core.eval_jaxpr(
        discharged_body_jaxpr.jaxpr,
        discharged_body_jaxpr.consts,
        *body_consts_and_refs,
        *carry,
    )
    carry, body_refs_out = split_list(body_carry_refs, [num_carry])
    return [*body_refs_out, *cond_refs_out, *carry]

  new_body_jaxpr, _ = pe.trace_to_jaxpr(
      new_body,
      FlatTree.flatten_args(*remaining_body_const_avals,
          *[a.inner_aval for a in body_ref_avals],
          *[a.inner_aval for a in cond_ref_avals],
          *carry_avals),
      debug_info=discharged_body_jaxpr.debug_info)
  if new_body_jaxpr.consts: raise NotImplementedError

  # Since some `Ref`s that were previously consts are now carries, we need to
  # deal with them (i.e. ignore them) in the `cond`, so we need to rewrite the
  # cond_jaxpr as well.
  def new_cond(*consts_refs_carry):
    consts, body_refs, cond_refs, carry = split_list(
        consts_refs_carry, [num_remaining_cond_consts, num_body_refs, num_cond_refs])
    # We don't use them here!
    del body_refs
    cond_consts_and_refs = merge_lists(cond_is_ref, consts, cond_refs)
    results = core.eval_jaxpr(
        discharged_cond_jaxpr.jaxpr,
        discharged_cond_jaxpr.consts,
        *cond_consts_and_refs,
        *carry,
    )
    predicate, refs_out = split_list(results, [1])
    assert len(refs_out) == len(cond_refs)
    return predicate

  new_cond_jaxpr, _ = pe.trace_to_jaxpr(
      new_cond,
      FlatTree.flatten_args(*remaining_cond_const_avals,
          *[a.inner_aval for a in body_ref_avals],
          *[a.inner_aval for a in cond_ref_avals],
          *carry_avals),
      debug_info=cond_jaxpr.debug_info.with_unknown_names())
  if new_cond_jaxpr.consts: raise NotImplementedError

  out = while_p.bind(*remaining_cond_consts, *remaining_body_consts,
                     *body_refs, *cond_refs, *carry,
                     body_jaxpr=new_body_jaxpr,
                     cond_jaxpr=new_cond_jaxpr,
                     body_nconsts=num_remaining_body_consts,
                     cond_nconsts=num_remaining_cond_consts)
  body_refs_out, cond_refs_out, carry_out = split_list(
      out, [num_body_refs, num_cond_refs])
  updated_cond_consts = merge_lists(cond_is_ref,
                                    [None] * num_remaining_cond_consts,
                                    cond_refs_out)
  updated_body_consts = merge_lists(body_is_ref,
                                    [None] * num_out_body_consts,
                                    body_refs_out)
  invals_out = [
      *updated_cond_consts,
      *updated_body_consts,
      *[None] * num_carry]
  return invals_out, carry_out

