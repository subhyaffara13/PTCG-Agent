
def create_joint_graph_node_information(
    joint_graph: Graph,
    recomputable_node_info: dict[str, int],
) -> dict[str, Any]:
    joint_graph_node_information: dict[str, Any] = {}

    for i, joint_graph_node in enumerate(joint_graph.nodes):
        is_recomputable_candidate: bool = (
            joint_graph_node.name in recomputable_node_info
        )
        tensor_meta = joint_graph_node.meta.get("tensor_meta")
        # pyrefly: ignore [implicit-any]
        shape = getattr(tensor_meta, "shape", []) if tensor_meta else []

        node_info: dict[str, Any] = {
            "index": i,
            "name": joint_graph_node.name,
            "is_recomputable_candidate": is_recomputable_candidate,
            "target": str(joint_graph_node.target),
            "shape": str(shape),
            "input_arguments": [inp.name for inp in joint_graph_node.all_input_nodes],
            "stack_trace": joint_graph_node.meta.get("stack_trace", ""),
        }

        if is_recomputable_candidate:
            idx: int = recomputable_node_info[joint_graph_node.name]
            node_info["recomputable_candidate_info"] = {
                "recomputable_node_idx": idx,
            }

        joint_graph_node_information[joint_graph_node.name] = node_info

    return joint_graph_node_information

