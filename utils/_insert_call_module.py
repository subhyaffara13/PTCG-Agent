
def _insert_call_module(
    gm: torch.fx.GraphModule,
    args_nodes: list[torch.fx.Node],
    kwargs_nodes: dict[str, torch.fx.Node],
    module_to_swap: torch.nn.Module,
    name: str,
) -> torch.fx.Node:
    from .unflatten import _assign_attr, _AttrKind

    _assign_attr(module_to_swap, gm, name, _AttrKind.MODULE)
    module_node = gm.graph.call_module(name, tuple(args_nodes), kwargs_nodes)  # type: ignore[arg-type]
    return module_node

