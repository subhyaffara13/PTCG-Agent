
def gen_pattern_and_search_gm(
    search_fn: SearchFn,
    example_inputs: Sequence[Any],
    trace_fn: TraceFn,
    scalar_workaround: dict[str, float | int] | None = None,
    exclusive_arg_names: Sequence[str] = (),
    get_decomp_fn: Callable[..., dict[Any, Callable[..., Any]]] = select_decomp_table,
) -> tuple[PatternExpr, torch.fx.GraphModule]:
    argnames = [*inspect.signature(search_fn).parameters.keys()]

    if scalar_workaround is None:
        scalar_workaround = {}
    flat_inputs = []
    input_idx = 0  # Positional arguments index

    for argname in argnames:
        if argname in scalar_workaround:
            flat_inputs.append(scalar_workaround[argname])
        else:
            flat_inputs.append(example_inputs[input_idx])
            input_idx += 1

    search_gm = trace_fn(search_fn, flat_inputs, get_decomp_fn=get_decomp_fn)
    return (
        fx_to_pattern(
            search_gm,
            ignore_types=(int, float, list, torch.device, torch.dtype),
            argnames=argnames,
            scalar_workaround=scalar_workaround,
            exclusive_arg_names=exclusive_arg_names,
        ),
        search_gm,
    )

