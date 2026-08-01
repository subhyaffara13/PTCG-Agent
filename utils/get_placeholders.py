
def get_placeholders(graph: fx.Graph) -> fx.graph._node_list:
    return graph.find_nodes(op="placeholder")

