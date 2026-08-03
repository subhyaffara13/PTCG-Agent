from typing import Any

def _graph_output_names(gm: torch.fx.GraphModule) -> list[Any]:
    output_node = next(iter(reversed(gm.graph.nodes)))
    if output_node.op != "output" or len(output_node.args) != 1:
        raise AssertionError(
            f"expected output node with 1 arg, got op={output_node.op}, args={len(output_node.args)}"
        )
    return_args = output_node.args[0]
    return [getattr(return_arg, "name", None) for return_arg in return_args]

