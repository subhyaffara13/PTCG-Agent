import logging

def remat_partial_eval(trace: pe.JaxprTrace, *tracers: core.Tracer,
                       jaxpr: core.Jaxpr, prevent_cse, **params):
  assert not jaxpr.constvars
  disallowed_effects = effects.remat_allowed_effects.filter_not_in(jaxpr.effects)
  if disallowed_effects:
    raise NotImplementedError(
        'Effects not supported in partial-eval of `checkpoint`/`remat`: '
        f'{disallowed_effects}')
  policy = params['policy'] or nothing_saveable
  in_unknowns = [not t.is_known() for t in tracers]
  jaxpr_known, jaxpr_staged, out_unknowns, out_inst, num_res = \
      pe.partial_eval_jaxpr_custom(
          jaxpr, in_unknowns, [True] * len(in_unknowns), False, False, policy)

  # DCE jaxpr_staged, keeping only instantiated outputs which are unknown
  _, out_inst_unknown = partition_list(out_inst, out_unknowns)
  jaxpr_unknown, in_used_staged = pe.dce_jaxpr(jaxpr_staged, out_inst_unknown)
  used_res, in_used_staged = split_list(in_used_staged, [num_res])

  # DCE jaxpr_known, keeping all known outputs but discarding dce'd res
  out_used_known = [True] * (len(out_unknowns) - sum(out_unknowns)) + used_res
  jaxpr_known, in_used_known = pe.dce_jaxpr(jaxpr_known, out_used_known)
  num_res = sum(used_res)

  # To avoid precision mismatches in fwd and bwd passes due to XLA excess
  # precision, insert explicit x = reduce_precision(x, **finfo(x.dtype)) calls
  # on producers of any residuals. See https://github.com/jax-ml/jax/pull/22244.
  jaxpr_known_ = _insert_reduce_precision(jaxpr_known, num_res)

  # Compute known outputs and residuals (hoisted out of remat primitive)
  _, in_consts_ = unzip2(t.pval for t in tracers if t.pval.is_known())
  _, in_consts = partition_list(in_used_known, in_consts_)
  out_consts = core.eval_jaxpr(jaxpr_known_, (), *in_consts)
  out_knowns, residuals = split_list(out_consts, [len(out_consts)-num_res])

  # set up unknown outputs with a recipe to call remat
  res_tracers = map(trace.new_instantiated_const, residuals)
  _, tracers_staged = partition_list(in_used_staged, tracers)
  in_jaxpr_tracers = res_tracers + map(trace.instantiate_const, tracers_staged)  # pyrefly: ignore[bad-argument-type]
  out_jaxpr_tracers = [pe.JaxprTracer(trace, pe.PartialVal.unknown(x.aval), None)
                       for x in jaxpr_unknown.outvars]
  if isinstance(prevent_cse, tuple):
    _, prevent_cse_ = partition_list(in_used_staged, prevent_cse)
    prevent_cse = (True,) * len(res_tracers) + tuple(prevent_cse_)
  new_params = dict(params, jaxpr=jaxpr_unknown, differentiated=True,
                    prevent_cse=prevent_cse)
  recipe = pe.new_eqn_recipe(trace, in_jaxpr_tracers, out_jaxpr_tracers, remat_p,
                             new_params, core.positional_effects(jaxpr_unknown),
                             source_info_util.current())

  # log info about saved residuals
  log_level = logging.WARNING if config.log_checkpoint_residuals.value else logging.DEBUG
  if logger.isEnabledFor(log_level):
    try:
      _, staged_unk = partition_list(in_used_staged, in_unknowns)
      res_invars, _ = partition_list(staged_unk, jaxpr_unknown.invars[num_res:])
      res_outvars = jaxpr_known.outvars[len(jaxpr_known.outvars) - num_res:]
      body_res = _saved_residuals(jaxpr_known.replace(outvars=res_outvars),
                                  ("",) * len(jaxpr_known.invars))
      logger.log(log_level,
                'remat-decorated function ' +
                'saving inputs with shapes:\n' * bool(res_invars) +
                '  %s\n' * len(res_invars) +
                'and ' * bool(res_invars) * bool(body_res) +
                'saving these intermediates:\n' * bool(body_res) +
                '  %s from %s\n' * len(body_res),
                *[v.aval.str_short() for v in res_invars],
                *[elt for (a, s) in body_res for elt in [a.str_short(), s]])
    except:
      pass  # just don't log anything on failure

  for t in out_jaxpr_tracers: t.recipe = recipe

  # zip together known and unknown outputs
  return merge_lists(out_unknowns, out_knowns, out_jaxpr_tracers)

