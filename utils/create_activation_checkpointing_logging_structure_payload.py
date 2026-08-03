from typing import Any

def create_activation_checkpointing_logging_structure_payload(
    joint_graph: Graph,
    joint_graph_node_information: dict[str, Any],
    joint_graph_edges: list[tuple[str, str]],
    all_recomputable_banned_nodes: list[Node],
    expected_runtime: float,
    saved_node_idxs: list[int],
    recomputable_node_idxs: list[int],
    memories_banned_nodes: list[int],
    normalized_memories_banned_nodes: list[float],
    runtimes_banned_nodes: list[float],
    min_cut_saved_values: list[Node],
) -> dict[str, Any]:
    """
    Creates a structured payload for logging activation checkpointing information.

    Args:
        joint_graph: The computational graph representing operations.
        joint_graph_node_information: Dictionary containing information about nodes in the joint graph.
        joint_graph_edges: List of edges in the joint graph represented as tuples of node names.
        all_recomputable_banned_nodes: List of nodes that are banned from recomputation.
        expected_runtime: Expected runtime of the computation.
        saved_node_idxs: Indices of nodes that are saved (not recomputed).
        recomputable_node_idxs: Indices of nodes that can be recomputed.
        memories_banned_nodes: Memory usage values (in absolute units) for banned nodes.
        normalized_memories_banned_nodes: Normalized memory usage values for banned nodes,
            used as input to the knapsack algorithm.
        runtimes_banned_nodes: Runtime values for banned nodes, used as input to the
            knapsack algorithm.
        min_cut_saved_values: List of nodes saved by the min-cut algorithm.

    Returns:
        A dictionary containing structured logging information for activation checkpointing.
    """
    activation_checkpointing_logging_structure_payload: dict[str, Any] = {
        "Joint Graph Size": len(joint_graph.nodes),
        "Joint Graph Edges": {
            "Total": len(joint_graph_edges),
            "Edges": joint_graph_edges,
        },
        "Joint Graph Node Information": joint_graph_node_information,
        "Recomputable Banned Nodes Order": [
            node.name for node in all_recomputable_banned_nodes
        ],
        "Expected Runtime": expected_runtime,
        "Knapsack Saved Nodes": saved_node_idxs,
        "Knapsack Recomputed Nodes": recomputable_node_idxs,
        "Absolute Memories": memories_banned_nodes,
        "Knapsack Input Memories": normalized_memories_banned_nodes,
        "Knapsack Input Runtimes": runtimes_banned_nodes,
        "Min Cut Solution Saved Values": [node.name for node in min_cut_saved_values],
    }
    return activation_checkpointing_logging_structure_payload

