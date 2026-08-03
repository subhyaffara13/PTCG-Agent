from typing import Any

def first_call_function_nn_module_stack(graph: torch.fx.Graph) -> dict[str, Any] | None:
    """
    Returns the nn_module_stack of the first call_function node.
    """
    for node in graph.nodes:
        if node.op == "call_function" and "nn_module_stack" in node.meta:
            return node.meta["nn_module_stack"]
    return None

