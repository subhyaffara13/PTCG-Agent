from typing import Any

def process_subgraph_nodes(graph_module: torch.fx.GraphModule, args: list[Any]):
    """Process nodes from a FX graph by executing them through V.graph.

    This is a common pattern for executing a subgraph's nodes:
    - Placeholder nodes are mapped to the provided args
    - Output nodes return their result
    - Other nodes are executed via V.graph.run_node

    """
    output = _MISSING

    for i, node in enumerate(graph_module.graph.nodes):
        if node.op == "placeholder":
            assert node not in V.graph.env
            V.graph.env[node] = args[i]
            continue
        elif node.op == "output":
            output_args, kwargs = V.graph.fetch_args_kwargs_from_env(node)
            output = torch.fx.Interpreter.output(V.graph, node, output_args, kwargs)
        else:
            assert node not in V.graph.env
            # Track current node for error diagnostics; restore after run_node to handle nested calls correctly
            saved_current_node = V.graph.current_node
            try:
                V.graph.current_node = node
                V.graph.env[node] = V.graph.run_node(node)
            finally:
                V.graph.current_node = saved_current_node

    if output is _MISSING:
        raise RuntimeError("No output node found in graph")

    return output

