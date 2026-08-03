from typing import Callable

def _shard_map_linearize(trace, shard_map_p, f: Callable,
                         tracers, mesh, in_specs, check_vma,
                         newly_manual_axes, debug_info):
  debug_info = debug_info.with_unknown_names()
  primals, tangents = unzip2(map(trace.to_primal_tangent_pair, tracers))
  nzs_in = tuple(type(t) is not ad.Zero for t in tangents)
  all_names = _all_newly_manual_mesh_names(mesh, newly_manual_axes)

  def f_lin(*primals):
    res, ans_aux, lin_data = ad.linearize_subtrace_2(
      f, trace.is_vjp, trace.tag, nzs_in, debug_info, primals)
    primals_out, out_specs = ans_aux.unpack_aux()

    res_avals, _, _, _, in_fwd, out_fwd = lin_data
    res_avals = [r for r, f1, f2 in zip(res_avals, in_fwd, out_fwd)
                 if f1 is None and f2 is None]
    res_specs = [a.nospec(mesh, check_vma, all_names) for a in res_avals]
    new_out_specs = (*res_specs, *out_specs)
    res = [lax.broadcast(x, (1,)) if not getattr(x, 'shape', ()) else x
           for x in res]
    res_and_primal = FlatTree.pack((FlatTree.flatten(res), primals_out))
    return res_and_primal.with_aux((lin_data, out_specs)).with_aux(new_out_specs)

  fwd_params = dict(
      mesh=mesh, in_specs=in_specs,
      check_vma=check_vma, newly_manual_axes=newly_manual_axes, debug_info=debug_info)
  avals = [typeof(x) for x in primals]
  all_results_aux = shard_map_p.bind_with_trace(
      trace.parent_trace, tuple(primals), avals, dict(fwd_params, subfuns=(f_lin,)))
  all_results, (lin_data, out_specs) = all_results_aux.unpack_aux()
  res_avals, nzs_out, lin_jaxpr, env, in_fwd, out_fwd = lin_data
  non_fwd_res, primals_out = all_results.unpack()
  residuals = subs_list2(in_fwd, out_fwd, primals, (*primals_out,), non_fwd_res)
  args_to_promote = [getattr(aval, 'shape', ()) == () and f1 is None and f2 is None
                     for aval, f1, f2 in zip(res_avals, in_fwd, out_fwd)]
  with (_extend_axis_env(mesh, newly_manual_axes),
        use_abstract_mesh(_as_manual_mesh(mesh, newly_manual_axes)),
        config._check_vma(check_vma)):
    lin_jaxpr = _promote_scalar_residuals_jaxpr(lin_jaxpr, args_to_promote)
  res_avals2 = [r for r, f1, f2 in zip(res_avals, in_fwd, out_fwd)
                if f1 is None and f2 is None]
  res_avals_iter = iter(res_avals2)
  res_specs = [in_specs[f1] if f1 is not None else out_specs[f2] if f2 is not None
               else next(res_avals_iter).nospec(mesh, check_vma, all_names)
               for f1, f2 in zip(in_fwd, out_fwd)]
  assert next(res_avals_iter, None) is None
  env_specs = [_repspec(typeof(e)) for e in env]
  new_in_specs = (*res_specs, *env_specs,
                  *(s.to_tangent_spec() for s, nz in zip(in_specs, nzs_in) if nz))
  tangent_out_specs = tuple(s.to_tangent_spec() for s, nz in zip(out_specs, nzs_out) if nz)
  tangent_params = dict(
      mesh=mesh, in_specs=new_in_specs,
      check_vma=check_vma, newly_manual_axes=newly_manual_axes,
      debug_info=lin_jaxpr.debug_info)

  # TODO(mattjj): avoid round-tripping the jaxpr through eval_jaxpr here
  def f_tangent(*args):
    ans = core.eval_jaxpr(lin_jaxpr, (), *args)
    return FlatTree.flatten(ans).with_aux(tangent_out_specs)

  nz_tangents_in = [t for (t, nz) in zip(tangents, nzs_in) if nz]
  args = (*residuals, *env, *nz_tangents_in)
  avals = [typeof(x) for x in args]
  nz_tangents_out = shard_map_p.bind_with_trace(
      trace.tangent_trace, args, avals,
      dict(tangent_params, subfuns=(f_tangent,)))
  nz_tangents_out_iter = iter(nz_tangents_out)
  tangents_out = [next(nz_tangents_out_iter) if nz else ad.p2tz(primal)
                  for nz, primal in zip(nzs_out, primals_out)]
  return primals_out.map3(partial(ad.maybe_linearize_tracer, trace), nzs_out, tangents_out)

