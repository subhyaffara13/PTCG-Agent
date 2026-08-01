
def has_cycle(G):
    """Decides whether the directed graph has a cycle."""
    try:
        # Feed the entire iterator into a zero-length deque.
        deque(topological_sort(G), maxlen=0)
    except nx.NetworkXUnfeasible:
        return True
    else:
        return False

