
def _directed_neighbor_switch_rev(
    G, w, unsat, h_node_residual_in, chords, h_partition_out, partition
):
    """The reverse of directed_neighbor_switch.

    Parameters
    ----------
    G : networkx directed graph
        graph within which the edge swap will take place.
    w : integer
        node id for which we need to perform a neighbor switch.
    unsat: set of integers
        set of node ids that have the same degree as w and are unsaturated.
    h_node_residual_in: dict of integers
        for a given node, keeps track of the remaining stubs to be added.
    chords: set of tuples
        keeps track of available positions to add edges.
    h_partition_out: dict of integers
        for a given node, keeps track of its partition id (out degree).
    partition: integer
        partition id to check if chords have to be updated.

    Notes
    -----
    Same operation as directed_neighbor_switch except it handles this operation
    for incoming edges instead of outgoing.
    """
    w_prime = unsat.pop()
    unsat.add(w_prime)
    # slightly faster declaring these as variables.
    w_neighbs = list(G.predecessors(w))
    w_prime_neighbs = list(G.predecessors(w_prime))
    # select node v, a neighbor of w, that is not connected to w_prime.
    for v in w_neighbs:
        if (v not in w_prime_neighbs) and w_prime != v:
            # removes (v,w), add (v,w_prime) and update data structures.
            G.remove_edge(v, w)
            G.add_edge(v, w_prime)
            if h_partition_out[v] == partition:
                chords.add((v, w))
                chords.discard((v, w_prime))

            h_node_residual_in[w] += 1
            h_node_residual_in[w_prime] -= 1
            if h_node_residual_in[w_prime] == 0:
                unsat.remove(w_prime)
            return None

    # If neighbor switch didn't work, use the unsaturated node.
    return w_prime

