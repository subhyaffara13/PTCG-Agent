
def _get_differentiable_graph_node(node, diff_node) -> None:
    if node.kind() == "prim::DifferentiableGraph":
        diff_node.append(node)
    else:
        for block in node.blocks():
            for n in block.nodes():
                _get_differentiable_graph_node(n, diff_node)

