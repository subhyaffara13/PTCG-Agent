
def hide_diedges(edges):
    """Returns a filter function that hides specific directed edges."""
    edges = {(u, v) for u, v in edges}
    return lambda u, v: (u, v) not in edges

