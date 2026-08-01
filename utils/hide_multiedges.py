
def hide_multiedges(edges):
    """Returns a filter function that hides specific multi-undirected edges."""
    alledges = set(edges) | {(v, u, k) for (u, v, k) in edges}
    return lambda u, v, k: (u, v, k) not in alledges

