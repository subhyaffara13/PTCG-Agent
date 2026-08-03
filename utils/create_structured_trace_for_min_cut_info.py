import json

def create_structured_trace_for_min_cut_info(
    joint_graph: Graph,
    all_recomputable_banned_nodes: list[Node],
    saved_node_idxs: list[int],
    recomputable_node_idxs: list[int],
    expected_runtime: float,
    memories_banned_nodes: list[int],
    normalized_memories_banned_nodes: list[float],
    runtimes_banned_nodes: list[float],
    min_cut_saved_values: list[Node],
) -> None:
    """
    Creates a structured trace for minimum cut information in the graph.

    Args:
        joint_graph: The computational graph representation.
        all_recomputable_banned_nodes: List of nodes that can be recomputed.
        saved_node_idxs: Indices of nodes that are saved in memory.
        recomputable_node_idxs: Indices of nodes that are recomputed.
        expected_runtime: Expected runtime for the computation.
        memories_banned_nodes: Memory requirements for each banned node in bytes.
        normalized_memories_banned_nodes: Normalized memory requirements for each banned node
            (typically scaled between 0 and 1 for relative comparison).
        runtimes_banned_nodes: Runtime costs associated with each banned node.
        min_cut_saved_values: Nodes that are saved as part of the minimum cut solution.
    """
    # Create a dictionary to store recomputable node information
    recomputable_node_info: dict[str, int] = {
        node.name: idx for idx, node in enumerate(all_recomputable_banned_nodes)
    }

    # Create joint graph node information
    joint_graph_node_information = create_joint_graph_node_information(
        joint_graph, recomputable_node_info
    )

    # Update node information with recomputable candidate details
    for node_name, node_info in joint_graph_node_information.items():
        if node_info["is_recomputable_candidate"]:
            idx = recomputable_node_info[node_name]
            node_info["recomputable_candidate_info"]["memory"] = memories_banned_nodes[
                idx
            ]
            node_info["recomputable_candidate_info"]["runtime"] = runtimes_banned_nodes[
                idx
            ]
            node_info["recomputable_candidate_info"]["is_saved"] = (
                idx in saved_node_idxs
            )
            node_info["recomputable_candidate_info"]["is_recomputed"] = (
                idx in recomputable_node_idxs
            )

    # Create joint graph edges
    joint_graph_edges = create_joint_graph_edges(joint_graph)

    # Create activation checkpointing logging structure payload
    activation_checkpointing_logging_structure_payload = (
        create_activation_checkpointing_logging_structure_payload(
            joint_graph=joint_graph,
            joint_graph_node_information=joint_graph_node_information,
            joint_graph_edges=joint_graph_edges,
            all_recomputable_banned_nodes=all_recomputable_banned_nodes,
            expected_runtime=expected_runtime,
            saved_node_idxs=saved_node_idxs,
            recomputable_node_idxs=recomputable_node_idxs,
            memories_banned_nodes=memories_banned_nodes,
            normalized_memories_banned_nodes=normalized_memories_banned_nodes,
            runtimes_banned_nodes=runtimes_banned_nodes,
            min_cut_saved_values=min_cut_saved_values,
        )
    )

    # Create structured trace
    trace_structured(
        "artifact",
        metadata_fn=lambda: {"name": "min_cut_information", "encoding": "json"},
        payload_fn=lambda: json.dumps(
            activation_checkpointing_logging_structure_payload
        ),
    )

