from typing import Any

def gen_gm_and_inputs(
    target: Any, args: list[Any], kwargs: dict[str, Any]
) -> tuple[GraphModule, list[torch.Tensor]]:
    g = torch.fx.Graph()
    graph_args: list[torch.Tensor] = []

    def add_tensor_arg(arg: torch.Tensor) -> Node:
        graph_args.append(arg)
        return g.placeholder(f"arg{len(graph_args)}")

    node = g.call_function(
        target, *tree_map_only(torch.Tensor, add_tensor_arg, (args, kwargs))
    )
    if (
        len(target._schema.returns) == 1
        and str(target._schema.returns[0].type) == "Tensor"
    ):
        node = (node,)  # type: ignore[assignment]
    g.output(node)

    gm = torch.fx.GraphModule({}, g)
    return gm, graph_args

