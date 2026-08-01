
def _quotient_graph(
    G, partition, edge_relation, node_data, edge_data, weight, relabel, create_using
):
    """Construct the quotient graph assuming input has been checked"""
    if create_using is None:
        H = G.__class__()
    else:
        H = nx.empty_graph(0, create_using)
    # By default set some basic information about the subgraph that each block
    # represents on the nodes in the quotient graph.
    if node_data is None:

        def node_data(b):
            S = G.subgraph(b)
            return {
                "graph": S,
                "nnodes": len(S),
                "nedges": S.number_of_edges(),
                "density": density(S),
            }

    # Each block of the partition becomes a node in the quotient graph.
    partition = [frozenset(b) for b in partition]
    H.add_nodes_from((b, node_data(b)) for b in partition)
    # By default, the edge relation is the relation defined as follows. B is
    # adjacent to C if a node in B is adjacent to a node in C, according to the
    # edge set of G.
    #
    # This is not a particularly efficient implementation of this relation:
    # there are O(n^2) pairs to check and each check may require O(log n) time
    # (to check set membership). This can certainly be parallelized.
    if edge_relation is None:

        def edge_relation(b, c):
            return any(v in G[u] for u, v in product(b, c))

    # By default, sum the weights of the edges joining pairs of nodes across
    # blocks to get the weight of the edge joining those two blocks.
    if edge_data is None:

        def edge_data(b, c):
            edgedata = (
                d
                for u, v, d in G.edges(b | c, data=True)
                if (u in b and v in c) or (u in c and v in b)
            )
            return {"weight": sum(d.get(weight, 1) for d in edgedata)}

    block_pairs = permutations(H, 2) if H.is_directed() else combinations(H, 2)
    # In a multigraph, add one edge in the quotient graph for each edge
    # in the original graph.
    if H.is_multigraph():
        edges = chaini(
            (
                (b, c, G.get_edge_data(u, v, default={}))
                for u, v in product(b, c)
                if v in G[u]
            )
            for b, c in block_pairs
            if edge_relation(b, c)
        )
    # In a simple graph, apply the edge data function to each pair of
    # blocks to determine the edge data attributes to apply to each edge
    # in the quotient graph.
    else:
        edges = (
            (b, c, edge_data(b, c)) for (b, c) in block_pairs if edge_relation(b, c)
        )
    H.add_edges_from(edges)
    # If requested by the user, relabel the nodes to be integers,
    # numbered in increasing order from zero in the same order as the
    # iteration order of `partition`.
    if relabel:
        # Can't use nx.convert_node_labels_to_integers() here since we
        # want the order of iteration to be the same for backward
        # compatibility with the nx.blockmodel() function.
        labels = {b: i for i, b in enumerate(partition)}
        H = nx.relabel_nodes(H, labels)
    return H

