from typing import Any

def get_ep_stats(ep: ExportedProgram) -> dict[str, Any]:
    op_count = 0
    op_set = set()
    for m in ep.graph_module.modules():
        if not isinstance(m, torch.fx.GraphModule):
            continue
        for node in m.graph.nodes:
            if node.op != "call_function":
                continue
            op_count += 1
            if not hasattr(node.target, "__module__"):
                raise AssertionError(
                    f"node.target {node.target} must have __module__ attribute"
                )
            if not hasattr(node.target, "__name__"):
                raise AssertionError(
                    f"node.target {node.target} must have __name__ attribute"
                )
            op_set.add(f"{node.target.__module__}.{node.target.__name__}")
    return {"op_count": op_count, "op_set": op_set}

