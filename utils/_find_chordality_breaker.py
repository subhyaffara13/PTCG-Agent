
def _find_chordality_breaker(G, s=None, treewidth_bound=sys.maxsize):
    """Given a graph G, starts a max cardinality search
    (starting from s if s is given and from an arbitrary node otherwise)
    trying to find a non-chordal cycle.

    If it does find one, it returns (u,v,w) where u,v,w are the three
    nodes that together with s are involved in the cycle.

    It ignores any self loops.
    """
    if len(G) == 0:
        raise nx.NetworkXPointlessConcept("Graph has no nodes.")
    unnumbered = set(G)
    if s is None:
        s = arbitrary_element(G)
    unnumbered.remove(s)
    numbered = {s}
    current_treewidth = -1
    while unnumbered:  # and current_treewidth <= treewidth_bound:
        v = _max_cardinality_node(G, unnumbered, numbered)
        unnumbered.remove(v)
        numbered.add(v)
        clique_wanna_be = set(G[v]) & numbered
        sg = G.subgraph(clique_wanna_be)
        if _is_complete_graph(sg):
            # The graph seems to be chordal by now. We update the treewidth
            current_treewidth = max(current_treewidth, len(clique_wanna_be))
            if current_treewidth > treewidth_bound:
                raise nx.NetworkXTreewidthBoundExceeded(
                    f"treewidth_bound exceeded: {current_treewidth}"
                )
        else:
            # sg is not a clique,
            # look for an edge that is not included in sg
            (u, w) = _find_missing_edge(sg)
            return (u, v, w)
    return ()

