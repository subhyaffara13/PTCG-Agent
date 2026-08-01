
def hide_nodes(nodes):
    """Returns a filter function that hides specific nodes."""
    nodes = set(nodes)
    return lambda node: node not in nodes

