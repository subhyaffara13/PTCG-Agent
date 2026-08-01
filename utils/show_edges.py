
def show_edges(edges):
    """Returns a filter function that shows specific undirected edges."""
    alledges = set(edges) | {(v, u) for (u, v) in edges}
    return lambda u, v: (u, v) in alledges

