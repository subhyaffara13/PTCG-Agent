
def _neighbor_switch(G, w, unsat, h_node_residual, avoid_node_id=None):
    """Releases one free stub for ``w``, while preserving joint degree in G.

    Parameters
    ----------
    G : NetworkX graph
        Graph in which the neighbor switch will take place.
    w : integer
        Node id for which we will execute this neighbor switch.
    unsat : set of integers
        Set of unsaturated node ids that have the same degree as w.
    h_node_residual: dictionary of integers
        Keeps track of the remaining stubs  for a given node.
    avoid_node_id: integer
        Node id to avoid when selecting w_prime.

    Notes
    -----
    First, it selects *w_prime*, an  unsaturated node that has the same degree
    as ``w``. Second, it selects *switch_node*, a neighbor node of ``w`` that
    is not  connected to *w_prime*. Then it executes an edge swap i.e. removes
    (``w``,*switch_node*) and adds (*w_prime*,*switch_node*). Gjoka et. al. [1]
    prove that such an edge swap is always possible.

    References
    ----------
    .. [1] M. Gjoka, B. Tillman, A. Markopoulou, "Construction of Simple
       Graphs with a Target Joint Degree Matrix and Beyond", IEEE Infocom, '15
    """

    if (avoid_node_id is None) or (h_node_residual[avoid_node_id] > 1):
        # select unsaturated node w_prime that has the same degree as w
        w_prime = next(iter(unsat))
    else:
        # assume that the node pair (v,w) has been selected for connection. if
        # - neighbor_switch is called for node w,
        # - nodes v and w have the same degree,
        # - node v=avoid_node_id has only one stub left,
        # then prevent v=avoid_node_id from being selected as w_prime.

        iter_var = iter(unsat)
        while True:
            w_prime = next(iter_var)
            if w_prime != avoid_node_id:
                break

    # select switch_node, a neighbor of w, that is not connected to w_prime
    w_prime_neighbs = G[w_prime]  # slightly faster declaring this variable
    for v in G[w]:
        if (v not in w_prime_neighbs) and (v != w_prime):
            switch_node = v
            break

    # remove edge (w,switch_node), add edge (w_prime,switch_node) and update
    # data structures
    G.remove_edge(w, switch_node)
    G.add_edge(w_prime, switch_node)
    h_node_residual[w] += 1
    h_node_residual[w_prime] -= 1
    if h_node_residual[w_prime] == 0:
        unsat.remove(w_prime)

