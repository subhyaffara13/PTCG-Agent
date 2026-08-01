
def is_tree_decomp(graph, decomp):
    """Check if the given tree decomposition is valid."""
    for x in graph.nodes():
        appear_once = False
        for bag in decomp.nodes():
            if x in bag:
                appear_once = True
                break
        assert appear_once

    # Check if each connected pair of nodes are at least once together in a bag
    for x, y in graph.edges():
        appear_together = False
        for bag in decomp.nodes():
            if x in bag and y in bag:
                appear_together = True
                break
        assert appear_together

    # Check if the nodes associated with vertex v form a connected subset of T
    for v in graph.nodes():
        subset = []
        for bag in decomp.nodes():
            if v in bag:
                subset.append(bag)
        sub_graph = decomp.subgraph(subset)
        assert nx.is_connected(sub_graph)

