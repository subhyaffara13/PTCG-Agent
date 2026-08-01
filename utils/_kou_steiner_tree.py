
def _kou_steiner_tree(G, terminal_nodes, weight):
    # Compute the metric closure only for terminal nodes
    # Create a complete graph H from the metric edges
    H = nx.Graph()
    unvisited_terminals = set(terminal_nodes)

    # check for connected graph while processing first node
    u = unvisited_terminals.pop()
    distances, paths = nx.single_source_dijkstra(G, source=u, weight=weight)
    if len(G) != len(distances):
        msg = "G is not a connected graph."
        raise nx.NetworkXError(msg)
    for v in unvisited_terminals:
        H.add_edge(u, v, distance=distances[v], path=paths[v])

    # first node done -- now process the rest
    for u in unvisited_terminals.copy():
        distances, paths = nx.single_source_dijkstra(G, source=u, weight=weight)
        unvisited_terminals.remove(u)
        for v in unvisited_terminals:
            H.add_edge(u, v, distance=distances[v], path=paths[v])

    # Use the 'distance' attribute of each edge provided by H.
    mst_edges = nx.minimum_spanning_edges(H, weight="distance", data=True)

    # Create an iterator over each edge in each shortest path; repeats are okay
    mst_all_edges = chain.from_iterable(pairwise(d["path"]) for u, v, d in mst_edges)
    if G.is_multigraph():
        mst_all_edges = (
            (u, v, min(G[u][v], key=lambda k: G[u][v][k].get(weight, 1)))
            for u, v in mst_all_edges
        )

    # Find the MST again, over this new set of edges
    G_S = G.edge_subgraph(mst_all_edges)
    T_S = nx.minimum_spanning_edges(G_S, weight="weight", data=False)

    # Leaf nodes that are not terminal might still remain; remove them here
    T_H = G.edge_subgraph(T_S).copy()
    _remove_nonterminal_leaves(T_H, terminal_nodes)

    return T_H.edges()

