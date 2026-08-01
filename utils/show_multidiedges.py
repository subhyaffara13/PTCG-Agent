
def show_multidiedges(edges):
    """Returns a filter function that shows specific multi-directed edges."""
    edges = {(u, v, k) for u, v, k in edges}
    return lambda u, v, k: (u, v, k) in edges

