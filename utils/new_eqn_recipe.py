from typing import Any

def new_eqn_recipe(trace: JaxprTrace,
                   in_tracers: Sequence[JaxprTracer],
                   out_tracers: Sequence[JaxprTracer],
                   primitive: Primitive,
                   params: dict[str, Any],
                   effects: core.Effects,
                   source_info: source_info_util.SourceInfo,
                   ctx: JaxprEqnContext | None = None) -> JaxprEqnRecipe:
  # TODO(necula): move these checks to core.check_jaxpr, and call in more places
  if primitive.call_primitive:
    assert "call_jaxpr" in params
    assert ("donated_invars" not in params or
            len(params["donated_invars"]) == len(params["call_jaxpr"].invars))
  out_avals = [t.aval for t in out_tracers]
  ctx = ctx or core.current_jaxpr_eqn_context()
  return JaxprEqnRecipe(next(trace.counter), tuple(in_tracers), map(ref, out_tracers),
                        out_avals, primitive, params, effects, source_info,
                        ctx)

