
def _is_separating_set(G, cut):
    """Assumes that the input graph is connected"""
    if len(cut) == len(G) - 1:
        return True

    H = nx.restricted_view(G, cut, [])
    if nx.is_connected(H):
        return False
    return True

