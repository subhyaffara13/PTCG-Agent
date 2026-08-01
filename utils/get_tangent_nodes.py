
def get_tangent_nodes(graph: Graph) -> Sequence[Node]:
    tangents = []
    for node in graph.find_nodes(op="placeholder", sort=False):
        if is_tangent_node(node):
            tangents.append(node)
    return tangents

