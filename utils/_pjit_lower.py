from typing import Any

def _pjit_lower(
    jaxpr: core.ClosedJaxpr,
    in_shardings,
    out_shardings,
    in_layouts: pxla.MaybeLayout,
    out_layouts: pxla.MaybeLayout,
    donated_invars,
    ctx_mesh,
    name: str,
    keep_unused: bool,
    inline: bool,
    compiler_options_kvs: tuple[tuple[str, Any], ...],
    *,
    lowering_platforms: tuple[str, ...] | None,
    lowering_parameters: mlir.LoweringParameters,
    pgle_profiler: profiler.PGLEProfiler | None) -> pxla.MeshComputation:
  return pxla.lower_sharding_computation(
      jaxpr, 'jit', name, in_shardings, out_shardings,
      in_layouts, out_layouts, tuple(donated_invars),
      keep_unused=keep_unused, context_mesh=ctx_mesh,
      compiler_options_kvs=compiler_options_kvs,
      lowering_platforms=lowering_platforms,
      lowering_parameters=lowering_parameters,
      pgle_profiler=pgle_profiler)

