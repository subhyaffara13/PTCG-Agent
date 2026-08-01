
def get_stack_traces(gm: torch.fx.GraphModule) -> list[str | None]:
    output = output_node(gm)
    assert len(output.args) == 1
    args = output.args[0]
    if not hasattr(args, "__iter__"):
        return []
    return [
        (arg.stack_trace if isinstance(arg, torch.fx.node.Node) else None)
        for arg in args  # type: ignore[union-attr]
    ]

