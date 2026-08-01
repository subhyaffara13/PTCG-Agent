
def _get_output_nodes(g: Graph) -> list[Node]:
    return [n for n in g.nodes if n.op == "output"]

