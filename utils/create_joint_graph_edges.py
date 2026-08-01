
def create_joint_graph_edges(joint_graph: Graph) -> list[tuple[str, str]]:
    joint_graph_edges: list[tuple[str, str]] = [
        (inp.name, node.name)
        for node in joint_graph.nodes
        for inp in node.all_input_nodes
    ]
    return joint_graph_edges

