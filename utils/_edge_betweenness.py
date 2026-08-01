
def _edge_betweenness(G, source, nodes=None, cutoff=False):
    """Edge betweenness helper."""
    # get the predecessor data
    (pred, length) = nx.predecessor(G, source, cutoff=cutoff, return_seen=True)
    # order the nodes by path length
    onodes = [n for n, d in sorted(length.items(), key=itemgetter(1))]
    # initialize betweenness, doesn't account for any edge weights
    between = {}
    for u, v in G.edges(nodes):
        between[(u, v)] = 1.0
        between[(v, u)] = 1.0

    while onodes:  # work through all paths
        v = onodes.pop()
        if v in pred:
            # Discount betweenness if more than one shortest path.
            num_paths = len(pred[v])
            for w in pred[v]:
                if w in pred:
                    # Discount betweenness, mult path
                    num_paths = len(pred[w])
                    for x in pred[w]:
                        between[(w, x)] += between[(v, w)] / num_paths
                        between[(x, w)] += between[(w, v)] / num_paths
    return between

