
def _while_partial_eval(trace: pe.JaxprTrace, *tracers: pe.Tracer, cond_nconsts: int,
                        cond_jaxpr: pe.ClosedJaxpr, body_nconsts: int,
                        body_jaxpr: pe.ClosedJaxpr) -> Sequence[pe.Tracer]:
  # As long as some carry (and hence output) are known and the output of
  # `cond_jaxpr` is known, we use a portion of the loop body to compute the
  # known outputs of the `while_loop`. For the unknown outputs we generate a
  # jaxpr to run the whole while, including recomputing the known parts,
  # basically like building in checkpointing/rematieralization. This means that
  # we don't actually save any computation by partial evaluation if there are
  # unknown outputs.
  #
  # What this achieves is twofold: jax.linearize works, and we can give a proper
  # error for reverse differentiation of `while`.

  unknowns = [not t.pval.is_known() for t in tracers]
  params = dict(cond_nconsts=cond_nconsts, cond_jaxpr=cond_jaxpr,
                body_nconsts=body_nconsts, body_jaxpr=body_jaxpr)

  cond_consts_uk, body_consts_uk, carry_init_uk = \
      split_list(unknowns, [cond_nconsts, body_nconsts])

  # Fixpoint computation of unknown carry. Each iteration promotes at least one
  # carry to unknown. We need one last iteration to prepare the jaxpr.
  carry_uk = carry_init_uk
  for _ in range(1 + len(carry_uk)):
    body_jaxpr_known, _, carry_out_uk, body_res_avals = pe.partial_eval_jaxpr_nounits(
        body_jaxpr, body_consts_uk + carry_uk, instantiate=carry_uk)
    if carry_out_uk == carry_uk:
      break
    else:
      carry_uk = _map(operator.or_, carry_uk, carry_out_uk)
  else:
    assert False, "Fixpoint not reached"

  cond_jaxpr_known, _, cond_uk, _ = pe.partial_eval_jaxpr_nounits(
      cond_jaxpr, cond_consts_uk + carry_uk, instantiate=False)

  if cond_uk[0] or all(not uk for uk in unknowns) or all(unknowns):
    # If conditional is unknown, or all inputs are known, or all are unknown,
    # just do the default processing.
    return trace.default_process_primitive(while_p, tracers, params)

  # Run the known part of the while.
  in_consts = [t.pval.get_known() for uk, t in
               zip(cond_consts_uk + body_consts_uk + carry_uk, tracers)
               if not uk]
  cond_nconsts_known = len(cond_consts_uk) - sum(cond_consts_uk)
  body_nconsts_known = len(body_consts_uk) - sum(body_consts_uk)
  num_known_outs = len(carry_uk) - sum(carry_uk)
  # TODO(mattjj): use pe.dce_jaxpr to drop res computations and not just outputs
  body_jaxpr_known = body_jaxpr_known.replace(
    jaxpr=body_jaxpr_known.jaxpr.replace(
      outvars=body_jaxpr_known.jaxpr.outvars[:num_known_outs]))
  out_known = while_p.bind(
      *in_consts, cond_nconsts=cond_nconsts_known, cond_jaxpr=cond_jaxpr_known,
      body_nconsts=body_nconsts_known, body_jaxpr=body_jaxpr_known)
  del body_jaxpr_known

  # Run the whole while_loop to get all the outputs, then merge with known ones
  out_tracers_ = trace.default_process_primitive(while_p, tracers, params)
  out_tracers = [t for t, uk in zip(out_tracers_, carry_uk) if uk]
  return util.merge_lists(carry_uk, out_known, out_tracers)

