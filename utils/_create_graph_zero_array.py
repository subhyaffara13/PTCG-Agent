
def _create_graph_zero_array(space: Graph):
    nodes = np.expand_dims(create_zero_array(space.node_space), axis=0)
    if space.edge_space is None:
        return GraphInstance(nodes=nodes, edges=None, edge_links=None)
    else:
        edges = np.expand_dims(create_zero_array(space.edge_space), axis=0)
        edge_links = np.zeros((1, 2), dtype=np.int64)
        return GraphInstance(nodes=nodes, edges=edges, edge_links=edge_links)

