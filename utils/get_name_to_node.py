
def get_name_to_node(graph: fx.Graph) -> dict[str, fx.Node]:
    name_to_node: dict[str, fx.Node] = {}
    for node in graph.nodes:
        name_to_node[node.name] = node
    return name_to_node

