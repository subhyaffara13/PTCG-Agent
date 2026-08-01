
def _is_space_graph_dtype_shape_equiv(space_1: Graph, space_2):
    return (
        isinstance(space_2, Graph)
        and is_space_dtype_shape_equiv(space_1.node_space, space_2.node_space)
        and (
            (space_1.edge_space is None and space_2.edge_space is None)
            or (
                space_1.edge_space is not None
                and space_2.edge_space is not None
                and is_space_dtype_shape_equiv(space_1.edge_space, space_2.edge_space)
            )
        )
    )

