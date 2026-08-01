
def _resolve_and_lower(
    args, jaxpr: core.ClosedJaxpr, in_shardings, out_shardings, in_layouts,
    out_layouts, donated_invars, ctx_mesh, name, keep_unused, inline,
    lowering_platforms, lowering_parameters, pgle_profiler,
    compiler_options_kvs) -> pxla.MeshComputation:
  in_shardings = _resolve_in_shardings(args, in_shardings)
  in_layouts = _resolve_in_layouts(args, in_layouts, in_shardings,
                                   jaxpr.in_avals)
  out_layouts = _resolve_out_layouts(out_layouts, out_shardings, jaxpr.out_avals)
  return _pjit_lower(
      jaxpr, in_shardings, out_shardings, in_layouts, out_layouts,
      donated_invars, ctx_mesh, name, keep_unused, inline, compiler_options_kvs,
      lowering_platforms=lowering_platforms,
      lowering_parameters=lowering_parameters,
      pgle_profiler=pgle_profiler)

