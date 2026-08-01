
def remove_self_clone(graph: Graph) -> None:
    for node in graph.nodes:
        if node.target is torch.ops.aten.copy_.default and node.args[0] == node.args[1]:
            node.replace_all_uses_with(node.args[0])
            graph.erase_node(node)

