from typing import Any

def create_node_from_old_node_preserve_meta(
    quantized_graph: Graph,
    create_node_args: tuple[Any, ...],
    old_node: Node,
) -> Node:
    """
    Creates `new_node` and copies the necessary metadata to it from `old_node`.
    """
    new_node = quantized_graph.create_node(*create_node_args)
    new_node.stack_trace = old_node.stack_trace
    return new_node

