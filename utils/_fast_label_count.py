
def _fast_label_count(G, comms, node, weight=None):
    """Computes the frequency of labels in the neighborhood of a node.

    Returns a dictionary keyed by label to the frequency of that label.
    """

    if weight is None:
        # Unweighted (un)directed simple graph.
        if not G.is_multigraph():
            label_freqs = Counter(map(comms.get, nx.all_neighbors(G, node)))

        # Unweighted (un)directed multigraph.
        else:
            label_freqs = defaultdict(int)
            for nbr in G[node]:
                label_freqs[comms[nbr]] += len(G[node][nbr])

            if G.is_directed():
                for nbr in G.pred[node]:
                    label_freqs[comms[nbr]] += len(G.pred[node][nbr])

    else:
        # Weighted undirected simple/multigraph.
        label_freqs = defaultdict(float)
        for _, nbr, w in G.edges(node, data=weight, default=1):
            label_freqs[comms[nbr]] += w

        # Weighted directed simple/multigraph.
        if G.is_directed():
            for nbr, _, w in G.in_edges(node, data=weight, default=1):
                label_freqs[comms[nbr]] += w

    return label_freqs

