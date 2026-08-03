from typing import Any

def gen_pattern(
    search_fn: SearchFn,
    example_inputs: Sequence[Any],
    trace_fn: TraceFn,
    scalar_workaround: dict[str, float | int] | None = None,
    exclusive_arg_names: Sequence[str] = (),
) -> PatternExpr:
    return gen_pattern_and_search_gm(
        search_fn, example_inputs, trace_fn, scalar_workaround, exclusive_arg_names
    )[0]

