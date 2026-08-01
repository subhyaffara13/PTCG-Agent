
def _shard_map_to_lojax(*hi_args, jaxpr, in_specs, out_specs, **params):
  mesh, newly_manual_axes = params['mesh'], params['newly_manual_axes']
  check_vma = params['check_vma']
  inner_mesh = _as_manual_mesh(mesh, newly_manual_axes)
  in_specs  = tuple(lo_spec for hi_spec in in_specs  for lo_spec in hi_spec.to_lo())
  lo_out_specs = tuple(lo_spec for hi_spec in out_specs for lo_spec in hi_spec.to_lo())
  lo_avals_ft = FlatTree.flatten(
      [[typeof(x) for x in typeof(hi_arg).lower_val(hi_arg)] for hi_arg in hi_args])
  lo_avals_ft = lo_avals_ft.map2(
      lambda a, s: shard_aval(mesh, newly_manual_axes, check_vma, s, a), in_specs)
  lo_avals_ft = FlatTree.pack((lo_avals_ft, {}))
  with (_extend_axis_env(mesh, newly_manual_axes), use_abstract_mesh(inner_mesh),
        config._check_vma(check_vma)):
    lo_jaxpr_, out_avals_ft = pe.lower_jaxpr(pe.close_jaxpr(jaxpr), lo_avals_ft)
    lo_jaxpr, consts = pe.separate_consts(lo_jaxpr_)
  out_avals_ft = out_avals_ft.map2(
      lambda a, s: unshard_aval(mesh, check_vma, s, a), lo_out_specs)
  trace = core.trace_ctx.trace
  source_info = source_info_util.current()
  to_jaxpr_tracer = partial(trace.to_jaxpr_tracer, source_info=source_info)
  const_tracers = map(to_jaxpr_tracer, consts)
  in_tracers = [to_jaxpr_tracer(loval) for arg in hi_args
                for loval in typeof(arg).lower_val(arg)]
  effs = core.filter_named_axis_effects(core.positional_effects(jaxpr),
                                        mesh.axis_names)
  out = trace.emit_eqn([*const_tracers, *in_tracers], list(out_avals_ft), shard_map_p,
                       dict(params, jaxpr=lo_jaxpr.jaxpr, in_specs=in_specs,
                            out_specs=lo_out_specs), effs, source_info)
  (), lo_outs = out_avals_ft.update(out).unpack()
  hi_out_avals = tuple(unshard_aval(mesh, check_vma, s, a)
                       for a, s in zip(jaxpr.out_avals, out_specs))
  return [a.raise_val2(y) for a, y in zip(hi_out_avals, lo_outs.unpack())]

