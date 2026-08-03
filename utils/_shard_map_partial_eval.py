from typing import Callable

def _shard_map_partial_eval(trace: pe.JaxprTrace, shard_map_p,
                            f: Callable, tracers, mesh, in_specs,
                            check_vma, newly_manual_axes, debug_info):
  tracers = map(trace.to_jaxpr_tracer, tracers)
  in_pvals = [t.pval for t in tracers]
  in_knowns, in_avals, in_consts = pe.partition_pvals(in_pvals)
  unk_in_specs, known_in_specs = pe.partition_list(in_knowns, in_specs)
  in_avals_sharded = map(partial(shard_aval, mesh, newly_manual_axes, check_vma),
                         unk_in_specs, in_avals)
  all_names = _all_newly_manual_mesh_names(mesh, newly_manual_axes)
  def f_pe(*in_consts):
    in_avals_, in_consts_ = iter(in_avals_sharded), iter(in_consts)
    in_pvals = [pe.PartialVal.known(next(in_consts_)) if known else
                pe.PartialVal.unknown(next(in_avals_)) for known in in_knowns]
    sentinel = object()
    assert next(in_avals_, sentinel) is next(in_consts_, sentinel) is sentinel
    jaxpr, fwd_data = pe.trace_to_subjaxpr_nounits_fwd2(
          f, trace.tag, debug_info.with_unknown_names(), False, in_pvals)
    (in_fwds, out_fwds, out_pvals, res, env) = fwd_data
    which = [f1 is None and f2 is None and not v.aval.shape
             for f1, f2, v in zip(in_fwds, out_fwds, jaxpr.constvars)]
    jaxpr = _promote_scalar_residuals_jaxpr(jaxpr, which)
    res = [lax.broadcast(x, (1,)) if not getattr(x, 'shape', ()) else x
           for x in res]
    out_pvals, out_specs = out_pvals.unpack_aux()
    out_knowns, _, out_consts = pe.partition_pvals(out_pvals)
    res_avals = [typeof(r) for r in res]
    _, out_known_specs = pe.partition_list(out_knowns, out_specs)
    res_specs = [a.nospec(mesh, check_vma, all_names) for a in res_avals]
    new_out_specs = (*out_known_specs, *res_specs)
    ft = out_pvals.map(lambda _: None)
    ans_ft = FlatTree.flatten((out_consts, res))
    aux = (in_fwds, out_fwds, out_knowns, res_avals, jaxpr, env, out_specs, new_out_specs, ft)
    return ans_ft.with_aux(aux).with_aux(new_out_specs)

  known_params = dict(mesh=mesh, in_specs=(*known_in_specs,),
                      check_vma=check_vma, newly_manual_axes=newly_manual_axes,
                      debug_info=debug_info.with_unknown_names())
  avals = [typeof(x) for x in in_consts]
  out = shard_map_p.bind_with_trace(trace.parent_trace, tuple(in_consts), avals,
                                    dict(known_params, subfuns=(f_pe,)))
  outs, (in_fwd, out_fwd, out_knowns, res_avals, jaxpr, env, out_specs, new_out_specs, ft) = out.unpack_aux()
  out_consts, non_fwd_res = outs.unflatten()

  assert not jaxpr.constvars
  unk_out_specs, _ = pe.partition_list(out_knowns, out_specs)
  res = subs_list2(in_fwd, out_fwd, in_consts, out_consts, non_fwd_res)
  # TODO make res_avals be the full set, not just the non-fwd ones
  res_avals_iter = iter(res_avals)
  res_specs = []
  for f1, f2 in zip(in_fwd, out_fwd):
    if f1 is not None:
      res_specs.append(known_in_specs[f1])
    elif f2 is not None:
      res_specs.append(new_out_specs[f2])
    else:
      raval = next(res_avals_iter)
      res_specs.append(raval.nospec(mesh, check_vma, all_names))
  env_specs = [_repspec(typeof(e)) for e in env]
  unk_in_specs = (*res_specs, *env_specs, *unk_in_specs)
  const_tracers = map(trace.new_instantiated_const, res)
  env_tracers = map(trace.to_jaxpr_tracer, env)
  unk_arg_tracers = [t for t in tracers if not t.is_known()]
  out_avals_sharded = [v.aval for v in jaxpr.outvars]
  unk_params = dict(mesh=mesh, in_specs=unk_in_specs,
                    out_specs=tuple(unk_out_specs),
                    jaxpr=jaxpr.replace(debug_info=jaxpr.debug_info.with_unknown_names()),
                    check_vma=check_vma, newly_manual_axes=newly_manual_axes)
  out_avals = map(partial(unshard_aval, mesh, check_vma), unk_out_specs,
                  out_avals_sharded)
  out_tracers = [pe.JaxprTracer(trace, pe.PartialVal.unknown(a), None)
                 for a in out_avals]
  effs = core.filter_named_axis_effects(core.positional_effects(jaxpr),
                                        mesh.axis_names)
  eqn = pe.new_eqn_recipe(trace, (*const_tracers, *env_tracers, *unk_arg_tracers),
                          out_tracers, shard_map_p, unk_params,
                          effs, source_info_util.current())
  for t in out_tracers: t.recipe = eqn
  results = merge_lists(out_knowns, out_tracers, out_consts)
  return ft.update(results)

