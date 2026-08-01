
def replace_target_nodes_with(
    fx_module: GraphModule,
    old_op: str,
    old_target: Target,
    new_op: str,
    new_target: Target,
):
    """
    Modifies all nodes in fx_module.graph.nodes which match the specified op code
    and target, and updates them to match the new op code and target.
    """
    new_graph = Graph()
    val_map: dict[Node, Node] = {}
    for node in fx_module.graph.nodes:
        if node.op == old_op and node.target == old_target:
            args = map_arg(node.args, lambda n: val_map[n])
            kwargs = map_arg(node.kwargs, lambda n: val_map[n])
            if not isinstance(args, tuple):
                raise AssertionError(f"Expected tuple, got {type(args)}")
            if not isinstance(kwargs, dict):
                raise AssertionError(f"Expected dict, got {type(kwargs)}")
            val_map[node] = new_graph.create_node(
                new_op, new_target, args, kwargs, node.name
            )
        else:
            val_map[node] = new_graph.node_copy(node, lambda n: val_map[n])
    fx_module.graph = new_graph

