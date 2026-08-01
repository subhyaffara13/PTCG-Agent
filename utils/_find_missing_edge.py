
def _find_missing_edge(G):
    """Given a non-complete graph G, returns a missing edge."""
    nodes = set(G)
    for u in G:
        missing = nodes - set(list(G[u].keys()) + [u])
        if missing:
            return (u, missing.pop())

