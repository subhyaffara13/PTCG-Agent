
def get_args_of_node_type(node: Node) -> Sequence[Node]:
    return [x for x in tree_flatten((node.args, node.kwargs))[0] if isinstance(x, Node)]

