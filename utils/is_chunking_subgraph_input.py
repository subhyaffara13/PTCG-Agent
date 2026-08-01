
def is_chunking_subgraph_input(node: Node) -> bool:
    meta = get_chunking_meta(node)
    if meta is None or is_tangent_node(node):
        return False
    arg_nodes = get_args_of_node_type(node)
    arg_nodes_no_meta = [node for node in arg_nodes if get_chunking_meta(node) is None]
    return len(arg_nodes_no_meta) > 0 or node.op == "placeholder"

