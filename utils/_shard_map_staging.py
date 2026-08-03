from typing import Any, Callable

def _shard_map_staging(
    trace: pe.DynamicJaxprTrace, prim: core.Primitive, f: Callable,
    args: Sequence[Any], *, mesh: Mesh, in_specs, check_vma: bool,
    newly_manual_axes: frozenset, debug_info) -> FlatTree:
  source_info = source_info_util.current()

  inner_mesh = _as_manual_mesh(mesh, newly_manual_axes)
  in_avals = [typeof(arg) for arg in args]
  in_avals_ = map(partial(shard_aval, mesh, newly_manual_axes, check_vma),
                  in_specs, in_avals)
  with (_extend_axis_env(mesh, newly_manual_axes), use_abstract_mesh(inner_mesh),
        config._check_vma(check_vma)):
    in_avals_flat_tree = FlatTree.flatten((in_avals_, {}))
    jaxpr, out_data = pe.trace_to_jaxpr(
        f, in_avals_flat_tree, debug_info, fun_returns_flat_tree=True,
        requires_low=trace.requires_low)
  out_avals_ft, out_specs = out_data.unpack_aux()
  _check_names(out_specs, out_avals_ft)
  if check_vma:
    _check_mats(mesh, out_specs, out_avals_ft)
  out_avals = [unshard_aval(mesh, check_vma, spec, aval)
               for spec, aval in zip(out_specs, out_avals_ft)]
  with (_extend_axis_env(mesh, newly_manual_axes), use_abstract_mesh(inner_mesh),
        config._check_vma(check_vma)):
    jaxpr, consts = pe.separate_consts(jaxpr)
  in_specs_staged = (*(_repspec(typeof(c)) for c in consts), *in_specs)
  if trace.requires_low:
    in_specs_staged = tuple(lo_spec for hi_spec in in_specs_staged
                            for lo_spec in hi_spec.to_lo())
    out_specs = tuple(lo_spec for hi_spec in out_specs
                      for lo_spec in hi_spec.to_lo())
  params = dict(mesh=mesh, in_specs=in_specs_staged,
                out_specs=out_specs, jaxpr=jaxpr.jaxpr,
                check_vma=check_vma, newly_manual_axes=newly_manual_axes)
  effs = core.filter_named_axis_effects(core.positional_effects(jaxpr),
                                        mesh.axis_names)
  to_jaxpr_tracer = partial(trace.to_jaxpr_tracer, source_info=source_info)
  const_tracers = map(to_jaxpr_tracer, consts)
  trace.frame.is_high |= jaxpr.is_high
  if trace.requires_low:
    in_tracers = [to_jaxpr_tracer(loval) for arg in args
                  for loval in typeof(arg).lower_val(arg)]
    out_avals_lo = [lo_aval for aval in out_avals for lo_aval in aval.lo_ty()]
  else:
    in_tracers = map(to_jaxpr_tracer, args)
    out_avals_lo = out_avals
  out = trace.emit_eqn([*const_tracers, *in_tracers], out_avals_lo, prim, params,
                       effs, source_info)
  if trace.requires_low:
    out = pe.raise_lo_outs(out_avals, out)
  return out_avals_ft.update(out)

