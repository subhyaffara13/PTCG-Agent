
def _pjit_partial_eval(trace: pe.JaxprTrace,
                       *in_tracers,
                       jaxpr: core.ClosedJaxpr, in_shardings, out_shardings,
                       in_layouts, out_layouts, donated_invars, ctx_mesh,
                       name, keep_unused, inline, compiler_options_kvs):
  in_pvals = [t.pval for t in in_tracers]
  known_ins = tuple(pv.is_known() for pv in in_pvals)
  unknown_ins = tuple(not k for k in known_ins)
  known_jaxpr, unknown_jaxpr, unknown_outs, res_out_avals, in_fwd_res = \
      pe.partial_eval_jaxpr_nounits_fwd(jaxpr, unknown_ins, instantiate=False)
  unknown_outs = tuple(unknown_outs)
  known_outs = tuple(not uk for uk in unknown_outs)

  # out_shardings and out_layouts for residual values output by known_jaxpr
  def keep_where(l, should_keep):
    return tuple(x for x, keep in zip(l, should_keep) if keep)

  known_out_shardings = (keep_where(out_shardings, known_outs)
                         + (UNSPECIFIED,) * len(res_out_avals))
  known_out_layouts = (keep_where(out_layouts, known_outs)
                       + (None,) * len(res_out_avals))

  # Input-to-output forwarding: compute which outputs are just forwarded inputs.
  num_out_primals = len(known_jaxpr.out_avals) - len(res_out_avals)
  in_fwd: list[int | None] = pe._jaxpr_forwarding(known_jaxpr.jaxpr)
  in_fwd_primal, in_fwd_res_ = split_list(in_fwd, [num_out_primals])
  assert all(f is None for f in in_fwd_res_)
  in_fwd = [
      fwd if isinstance(os, UnspecifiedValue) and ol is None else None
      for os, ol, fwd in zip(
          keep_where(out_shardings, known_outs),
          keep_where(out_layouts, known_outs), in_fwd_primal)
  ] + in_fwd_res_
  del in_fwd_primal, in_fwd_res_
  # Prune jaxpr outputs and out_shardings by removing the input-forwards.
  keep = [f is None for f in in_fwd]
  known_jaxpr = pe.prune_closed_jaxpr_outputs(known_jaxpr, keep)
  known_out_shardings = keep_where(known_out_shardings, keep)
  known_out_layouts = keep_where(known_out_layouts, keep)
  # Update num_out_primals to reflect pruning.
  kept_primals, kept_res = split_list(keep, [num_out_primals])
  num_out_primals = sum(kept_primals)
  del keep, kept_primals, kept_res

  # Output-to-output forwarding: compute which residuals are just primal outputs
  out_vars, res_vars = split_list(known_jaxpr.jaxpr.outvars, [num_out_primals])
  idx_map = {id(v): i for i, v in enumerate(out_vars)}
  out_fwd = [None] * num_out_primals + [idx_map.get(id(v)) for v in res_vars]
  # Prune jaxpr outputs and out_shardings by removing forwarded residuals.
  keep = [f is None for f in out_fwd]
  known_jaxpr = pe.prune_closed_jaxpr_outputs(known_jaxpr, keep)
  known_out_shardings = keep_where(known_out_shardings, keep)
  known_out_layouts = keep_where(known_out_layouts, keep)
  del keep

  known_params = dict(
      jaxpr=known_jaxpr, in_shardings=keep_where(in_shardings, known_ins),
      out_shardings=known_out_shardings,
      in_layouts=keep_where(in_layouts, known_ins),
      out_layouts=known_out_layouts,
      donated_invars=keep_where(donated_invars, known_ins),
      ctx_mesh=ctx_mesh,
      name=name, keep_unused=keep_unused, inline=inline,
      compiler_options_kvs=compiler_options_kvs)
  assert len(known_params['out_shardings']) == len(known_params['jaxpr'].out_avals)
  assert len(known_params['out_layouts']) == len(known_params['jaxpr'].out_avals)

  # Bind known things to pjit_p.
  known_inputs = [pv.get_known() for pv in in_pvals if pv.is_known()]
  all_known_outs = jit_p.bind(*known_inputs, **known_params)
  # Add back in the output fwds.
  all_known_outs = subs_list(out_fwd, all_known_outs, all_known_outs)
  # Add back in the input fwds.
  all_known_outs = subs_list(in_fwd, known_inputs, all_known_outs)

  known_out_vals, residual_vals = split_list(
      all_known_outs, [len(all_known_outs) - len(res_out_avals)])
  residual_vals_ = iter(residual_vals)
  residual_vals = [next(residual_vals_) if f is None
                   else [*jaxpr.consts, *known_inputs][f] for f in in_fwd_res]
  assert next(residual_vals_, None) is None
  residual_tracers = map(trace.new_instantiated_const, residual_vals)

  # The convention of partial_eval_jaxpr_nounits is to place residual binders at
  # the front of the jaxpr produced, so we move them to the back since both the
  # jaxpr equation built below and the pjit transpose rule assume a
  # residual-inputs-last convention.
  unknown_jaxpr = pe.move_binders_to_back(
      unknown_jaxpr, [True] * len(residual_vals) + [False] * sum(unknown_ins))

  # Set up staged-out 'unknown' eqn
  unknown_in_shardings = (keep_where(in_shardings, unknown_ins)
                          + (UNSPECIFIED,) * len(residual_tracers))
  unknown_in_layouts = (keep_where(in_layouts, unknown_ins)
                        + (None,) * len(residual_tracers))
  unknown_donated_invars = (keep_where(donated_invars, unknown_ins)
                            + (False,) * len(residual_tracers))
  unknown_params = dict(
      jaxpr=unknown_jaxpr,
      in_shardings=unknown_in_shardings,
      in_layouts=unknown_in_layouts,
      out_shardings=keep_where(out_shardings, unknown_outs),
      out_layouts=keep_where(out_layouts, unknown_outs),
      donated_invars=unknown_donated_invars,
      ctx_mesh=ctx_mesh,
      name=name,
      keep_unused=keep_unused,
      inline=inline,
      compiler_options_kvs=compiler_options_kvs)
  unknown_tracers_in = [t for t in in_tracers if not t.pval.is_known()]
  unknown_out_avals = unknown_jaxpr.out_avals
  unknown_tracers_out = [
      pe.JaxprTracer(trace, pe.PartialVal.unknown(aval), None)
      for aval in unknown_out_avals
  ]
  unknown_tracers_in = [*unknown_tracers_in, *residual_tracers]
  eqn = pe.new_eqn_recipe(trace, unknown_tracers_in,
                          unknown_tracers_out,
                          jit_p,
                          unknown_params,
                          core.positional_effects(unknown_jaxpr),
                          source_info_util.current())
  for t in unknown_tracers_out: t.recipe = eqn
  if effects_lib.partial_eval_kept_effects.filter_in(unknown_jaxpr.effects):
    trace.effect_handles.append(pe.EffectHandle(unknown_tracers_in, eqn))
  return merge_lists(unknown_outs, known_out_vals, unknown_tracers_out)

