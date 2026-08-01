
def _check_isomorphism(t1, t2, isomorphism):
    assert nx.is_directed(t1) == nx.is_directed(t2)
    # Apply mapping and check for equality
    H = nx.relabel_nodes(t1, dict(isomorphism))
    return nx.utils.graphs_equal(t2, H)

