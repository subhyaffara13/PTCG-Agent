
def _calculate_local_modularity_for_candidate(G, v, C, B, T, I):
    """
    Compute the local modularity R and updated variables when adding node v to the community.

    Parameters
    ----------
    G : NetworkX graph
        The input graph.
    v : node
        The candidate node to add to the community.
    C : set
        The current set of community nodes.
    B : set
        The current set of boundary nodes.
    T : set of frozenset
        The current set of boundary edges.
    I : set of frozenset
        The current set of internal boundary edges.

    Returns
    -------
    R_tmp : float
        The local modularity after adding node v.
    B_tmp : set
        The updated set of boundary nodes.
    T_tmp : set of frozenset
        The updated set of boundary edges.
    I_tmp : set of frozenset
        The updated set of internal boundary edges.
    """
    C_tmp = C | {v}
    B_tmp = B.copy()
    T_tmp = T.copy()
    I_tmp = I.copy()
    removed_B_nodes = set()

    # Update boundary nodes and edges
    for nbr in G[v]:
        if nbr not in C_tmp:
            # v has nbrs not in the community, so it remains a boundary node
            B_tmp.add(v)
            # Add edge between v and nbr to boundary edges
            T_tmp.add(frozenset([v, nbr]))

        if nbr in B:
            # Check if nbr should be removed from boundary nodes
            # Go through nbrs nbrs to see if it is still a boundary node
            nbr_still_in_B = any(nbr_nbr not in C_tmp for nbr_nbr in G[nbr])
            if not nbr_still_in_B:
                B_tmp.remove(nbr)
                removed_B_nodes.add(nbr)

        if nbr in C_tmp:
            # Add edge between v and nbr to internal edges
            I_tmp.add(frozenset([v, nbr]))

    # Remove edges no longer in the boundary
    for removed_node in removed_B_nodes:
        for removed_node_nbr in G[removed_node]:
            if removed_node_nbr not in B_tmp:
                T_tmp.discard(frozenset([removed_node_nbr, removed_node]))
                I_tmp.discard(frozenset([removed_node_nbr, removed_node]))

    R_tmp = len(I_tmp) / len(T_tmp) if len(T_tmp) > 0 else 1
    return R_tmp, B_tmp, T_tmp, I_tmp

