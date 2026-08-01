
def hide_edges(edges):
    """Returns a filter function that hides specific undirected edges."""
    alledges = set(edges) | {(v, u) for (u, v) in edges}
    return lambda u, v: (u, v) not in alledges

