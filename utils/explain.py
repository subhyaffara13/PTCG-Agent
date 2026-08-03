import logging
from typing import Any, Callable

def explain(f: Callable[..., Any], *extra_args: Any, **extra_kwargs: Any) -> Any:
    from .backends.debugging import ExplainOutput

    def inner(*args: Any, **kwargs: Any) -> ExplainOutput:
        # TODO(voz): Do we want a decorator for this?
        from . import reset  # type: ignore[attr-defined]

        reset()

        graphs: list[torch.fx.GraphModule] = []
        break_reasons: list[Any] = []
        op_count: int = 0
        ops_per_graph: list[list[Target]] = []
        out_guards: list[_guards.Guard] = []

        def dynamo_graph_accumulating_compiler(
            gm: torch.fx.GraphModule, example_inputs: Any
        ) -> Callable[..., Any]:
            from .backends.debugging import _explain_graph_detail

            nonlocal graphs
            nonlocal op_count
            nonlocal ops_per_graph
            nonlocal break_reasons

            gm, graphs, op_count, ops_per_graph, break_reasons = _explain_graph_detail(
                gm, graphs, op_count, ops_per_graph, break_reasons
            )

            return gm.forward

        def guard_export_print(guards: Iterable[_guards.Guard]) -> None:
            nonlocal out_guards
            out_guards.extend(guards)

        opt_f = optimize(
            dynamo_graph_accumulating_compiler,
            nopython=False,
            guard_export_fn=guard_export_print,
        )(f)
        # TODO(voz): We may have instances of `f` that mutate inputs, we should track sideeffects and reject.
        opt_f(*args, **kwargs)

        graph_count = len(graphs)
        graph_break_count = graph_count - 1
        compile_time = compile_times(repr="str")

        # TODO(voz): Do we want a decorator for this?
        reset()

        return ExplainOutput(
            graphs,
            graph_count,
            graph_break_count,
            break_reasons,
            op_count,
            ops_per_graph,
            out_guards,
            compile_time,
        )

    if extra_args or extra_kwargs:
        warnings.warn(
            "explain(f, *args, **kwargs) is deprecated, use explain(f)(*args, **kwargs) instead.  "
            "If you don't migrate, we may break your explain call in the future if your user defined kwargs "
            "conflict with future kwargs added to explain(f).",
            FutureWarning,
            stacklevel=2,
        )
        return inner(*extra_args, **extra_kwargs)
    else:
        return inner


def explain(keys, fun, in_avals, debug_info, *context, **_):
  func_filename = debug_info.func_filename
  if func_filename and not source_info_util.is_user_filename(func_filename):
   return

  msg: list[str] = []
  p = msg.append

  callsite = source_info_util.summarize(source_info_util.current())
  p(f"TRACING CACHE MISS at {callsite}:")

  src_info = ""
  if func_filename:
    src_info += f" defined at {func_filename}"
  if func_lineno := debug_info.func_lineno:
    src_info += f":{func_lineno}"
  func_name = debug_info.func_name

  # have we seen this function before at all?
  keys = [key for fun_ref, *key in keys if fun_ref() is fun]
  if not keys:
    p(f"  never seen function:\n    {func_name} id={id(fun)}{src_info}")
    if callsite in callsites_with_tracing_cache_miss:
      p("  but seen another function defined on the same line; maybe the function is\n"
        "  being re-defined repeatedly, preventing caching?")
    else:
      callsites_with_tracing_cache_miss.add(callsite)
    return logger.log(logging.WARNING, "\n".join(msg))

  p(f"  for {func_name}{src_info}")

  key = (config.trace_context(), (in_avals, debug_info, *context), {})
  min_diff = min(diff_tracing_cache_keys(key, k) for k in keys)[-1]
  p('  all previously seen cache keys differ. For the closest previous key:')
  p('  ' + min_diff)
  return logger.log(logging.WARNING, "\n".join(msg))

