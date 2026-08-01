
def erase_nodes(gm: GraphModule, nodes: NodeList) -> None:
    # erase original nodes in inversed topological order
    for node in reversed(nodes):
        gm.graph.erase_node(node)

