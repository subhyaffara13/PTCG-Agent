
def _flatten_space_graph(space: Graph) -> Graph:
    return Graph(
        node_space=flatten_space(space.node_space),
        edge_space=(
            flatten_space(space.edge_space) if space.edge_space is not None else None
        ),
    )


def _flatten_space_graph(space: Graph) -> Graph:
    return Graph(
        node_space=flatten_space(space.node_space),
        edge_space=flatten_space(space.edge_space)
        if space.edge_space is not None
        else None,
    )

