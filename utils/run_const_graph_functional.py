
def run_const_graph_functional(
    ctx: "BaseFunctionalizeAPI", graph: torch.fx.GraphModule, args: tuple[Any, ...]
) -> Any:
    unwrapped_args = ctx.unwrap_tensors(args)

    with ctx.redispatch_to_next():
        out = run_const_graph(graph, unwrapped_args)
        return ctx.wrap_tensors(out)  # type: ignore[arg-type]

