
def show_diedges(edges):
    """Returns a filter function that shows specific directed edges."""
    edges = {(u, v) for u, v in edges}
    return lambda u, v: (u, v) in edges

