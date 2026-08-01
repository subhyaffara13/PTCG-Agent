
def _create_empty_array_graph(
    space: Graph, n: int = 1, fn=np.zeros
) -> tuple[GraphInstance, ...]:
    if space.edge_space is not None:
        return tuple(
            GraphInstance(
                nodes=fn((1,) + space.node_space.shape, dtype=space.node_space.dtype),
                edges=fn((1,) + space.edge_space.shape, dtype=space.edge_space.dtype),
                edge_links=fn((1, 2), dtype=np.int64),
            )
            for _ in range(n)
        )
    else:
        return tuple(
            GraphInstance(
                nodes=fn((1,) + space.node_space.shape, dtype=space.node_space.dtype),
                edges=None,
                edge_links=None,
            )
            for _ in range(n)
        )

