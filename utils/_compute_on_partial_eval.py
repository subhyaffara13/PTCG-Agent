
def _compute_on_partial_eval(trace: pe.JaxprTrace, *in_tracers, jaxpr,
                             compute_type, out_memory_spaces,
                             compiler_options_json):
  in_pvals = [t.pval for t in in_tracers]
  known_ins = tuple(pv.is_known() for pv in in_pvals)
  unknown_ins = tuple(not k for k in known_ins)

  (known_jaxpr, unknown_jaxpr, unknown_outs, res_out_avals,
   in_fwd_res) = pe.partial_eval_jaxpr_nounits_fwd(
       jaxpr, unknown_ins, instantiate=False)
  unknown_outs = tuple(unknown_outs)
  known_outs = tuple(not uk for uk in unknown_outs)

  def keep_where(l, should_keep):
    return tuple(x for x, keep in zip(l, should_keep) if keep)

  known_out_memory_spaces = (keep_where(out_memory_spaces, known_outs)
                             + (core.MemorySpace.Device,) * len(res_out_avals))
  known_params = dict(jaxpr=known_jaxpr, compute_type=compute_type,
                      out_memory_spaces=known_out_memory_spaces,
                      compiler_options_json=compiler_options_json)

  known_inputs = [pv.get_known() for pv in in_pvals if pv.is_known()]
  all_known_outs = compute_on_p.bind(*known_inputs, **known_params)

  known_out_vals, residual_vals = split_list(
      all_known_outs, [len(all_known_outs) - len(res_out_avals)])
  residual_vals_ = iter(residual_vals)
  residual_vals = [next(residual_vals_) if f is None
                   else [*jaxpr.consts, *known_inputs][f] for f in in_fwd_res]
  assert next(residual_vals_, None) is None
  residual_tracers = map(trace.new_instantiated_const, residual_vals)

  unknown_params = dict(
      jaxpr=unknown_jaxpr, compute_type=compute_type,
      out_memory_spaces=keep_where(out_memory_spaces, unknown_outs),
      compiler_options_json=compiler_options_json)

  unknown_tracers_in = [*residual_tracers,
                        *(t for t in in_tracers if not t.pval.is_known())]
  unknown_out_avals = unknown_jaxpr.out_avals
  unknown_tracers_out = [
      pe.JaxprTracer(trace, pe.PartialVal.unknown(aval), None)
      for aval in unknown_out_avals
  ]
  eqn = pe.new_eqn_recipe(trace, unknown_tracers_in,
                          unknown_tracers_out,
                          compute_on_p,
                          unknown_params,
                          core.positional_effects(unknown_jaxpr),
                          source_info_util.current())
  for t in unknown_tracers_out: t.recipe = eqn
  if effects_lib.partial_eval_kept_effects.filter_in(unknown_jaxpr.effects):
    trace.effect_handles.append(pe.EffectHandle(unknown_tracers_in, eqn))
  return merge_lists(unknown_outs, known_out_vals, unknown_tracers_out)

