
def _low_degree_nodes(G, k, nbunch=None):
    """Helper for finding nodes with degree less than k."""
    # Nodes with degree less than k cannot be k-edge-connected.
    if G.is_directed():
        # Consider both in and out degree in the directed case
        seen = set()
        for node, degree in G.out_degree(nbunch):
            if degree < k:
                seen.add(node)
                yield node
        for node, degree in G.in_degree(nbunch):
            if node not in seen and degree < k:
                seen.add(node)
                yield node
    else:
        # Only the degree matters in the undirected case
        for node, degree in G.degree(nbunch):
            if degree < k:
                yield node

