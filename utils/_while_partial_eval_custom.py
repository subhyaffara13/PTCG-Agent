
def _while_partial_eval_custom(saveable, unks_in, inst_in, eqn):
  del saveable  # We can't save any residuals anyway (w/o dynamic shapes)!
  cond_jaxpr = eqn.params['cond_jaxpr']
  cond_nconsts = eqn.params['cond_nconsts']
  body_jaxpr = eqn.params['body_jaxpr']
  body_nconsts = eqn.params['body_nconsts']

  cond_consts_uk, body_consts_uk, carry_init_uk = \
      split_list(unks_in, [cond_nconsts, body_nconsts])

  # Fixpoint to compute known part of the body (trivial on 'inst_in', since we
  # make all inputs available as DCE can subsequently prune any unused ones)
  carry_uk = carry_init_uk
  for _ in range(1 + len(carry_uk)):
    body_unks_in = body_consts_uk + carry_uk
    jaxpr_known_, _, carry_uk_out, _, num_res = \
        pe.partial_eval_jaxpr_custom(
            body_jaxpr.jaxpr, in_unknowns=body_unks_in, in_inst=True,
            ensure_out_unknowns=carry_uk, ensure_out_inst=True,
            saveable=ad_checkpoint.nothing_saveable)
    if carry_uk_out == carry_uk:
      break
    else:
      carry_uk = _map(operator.or_, carry_uk, carry_uk_out)
  else:
    assert False, "Fixpoint not reached"
  assert not num_res
  body_jaxpr_known = ClosedJaxpr(jaxpr_known_, body_jaxpr.consts)
  del jaxpr_known_, carry_uk_out, num_res, unks_in

  # Instantiate all inputs (b/c jaxpr_staged will take all inputs).
  new_inst = [x for x, inst in zip(eqn.invars, inst_in)
              if type(x) is core.Var and not inst]

  # Compute the known part of cond_fun (basically pruning inputs on known side).
  cond_unks_in = cond_consts_uk + carry_uk
  cond_jaxpr_known_, _, [cond_uk], _, _ = \
      pe.partial_eval_jaxpr_custom(
          cond_jaxpr.jaxpr, cond_unks_in, in_inst=True,
          ensure_out_unknowns=False, ensure_out_inst=True,
          saveable=ad_checkpoint.nothing_saveable)
  # NOTE(mattjj): I think it should be impossible for the condition to be
  # unknown, but asserting that caused a test failure in diffrax. So
  # we handle it: if it is unknown, stage out the whole cond function.
  if cond_uk:
    return None, eqn, [True] * len(carry_uk), [True] * len(carry_uk), new_inst
  cond_jaxpr_known = ClosedJaxpr(cond_jaxpr_known_, cond_jaxpr.consts)
  del cond_uk

  # Build the known eqn.
  unks_in = [*cond_consts_uk, *body_consts_uk, *carry_uk]  # fixpoint carry_uk
  ins_known, _ = partition_list(unks_in, eqn.invars)
  out_binders_known, _ = partition_list(carry_uk, eqn.outvars)
  params_known = dict(cond_jaxpr=cond_jaxpr_known, body_jaxpr=body_jaxpr_known,
                      cond_nconsts=len(cond_consts_uk) - sum(cond_consts_uk),
                      body_nconsts=len(body_consts_uk) - sum(body_consts_uk))
  effects_known = _join_while_effects(body_jaxpr_known, cond_jaxpr_known,
                                      params_known['body_nconsts'],
                                      params_known['cond_nconsts'])
  eqn_known = pe.new_jaxpr_eqn(ins_known, out_binders_known, while_p,
                               params_known, effects_known, eqn.source_info,
                               eqn.ctx)
  # Typecheck known eqn.
  _while_loop_abstract_eval(
      *[v.aval for v in eqn_known.invars], cond_jaxpr=cond_jaxpr_known,
      body_jaxpr=body_jaxpr_known, body_nconsts=params_known['body_nconsts'],
      cond_nconsts=params_known['cond_nconsts'])

  # Staged eqn is same as input eqn.
  eqn_staged = eqn

  unks_out = carry_uk
  inst_out = [True] * len(unks_out)
  return eqn_known, eqn_staged, unks_out, inst_out, new_inst

