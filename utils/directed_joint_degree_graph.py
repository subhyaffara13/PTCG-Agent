
def directed_joint_degree_graph(in_degrees, out_degrees, nkk, seed=None):
    """Generates a random simple directed graph with the joint degree.

    Parameters
    ----------
    degree_seq :  list of tuples (of size 3)
        degree sequence contains tuples of nodes with node id, in degree and
        out degree.
    nkk  :  dictionary of dictionary of integers
        directed joint degree dictionary, for nodes of out degree k (first
        level of dict) and nodes of in degree l (second level of dict)
        describes the number of edges.
    seed : hashable object, optional
        Seed for random number generator.

    Returns
    -------
    G : Graph
        A directed graph with the specified inputs.

    Raises
    ------
    NetworkXError
        If degree_seq and nkk are not realizable as a simple directed graph.


    Notes
    -----
    Similarly to the undirected version:
    In each iteration of the "while loop" the algorithm picks two disconnected
    nodes v and w, of degree k and l correspondingly,  for which nkk[k][l] has
    not reached its target yet i.e. (for given k,l): n_edges_add < nkk[k][l].
    It then adds edge (v,w) and always increases the number of edges in graph G
    by one.

    The intelligence of the algorithm lies in the fact that  it is always
    possible to add an edge between disconnected nodes v and w, for which
    nkk[degree(v)][degree(w)] has not reached its target, even if one or both
    nodes do not have free stubs. If either node v or w does not have a free
    stub, we perform a "neighbor switch", an edge rewiring move that releases a
    free stub while keeping nkk the same.

    The difference for the directed version lies in the fact that neighbor
    switches might not be able to rewire, but in these cases unsaturated nodes
    can be reassigned to use instead, see [1] for detailed description and
    proofs.

    The algorithm continues for E (number of edges in the graph) iterations of
    the "while loop", at which point all entries of the given nkk[k][l] have
    reached their target values and the construction is complete.

    References
    ----------
    [1] B. Tillman, A. Markopoulou, C. T. Butts & M. Gjoka,
        "Construction of Directed 2K Graphs". In Proc. of KDD 2017.

    Examples
    --------
    >>> in_degrees = [0, 1, 1, 2]
    >>> out_degrees = [1, 1, 1, 1]
    >>> nkk = {1: {1: 2, 2: 2}}
    >>> G = nx.directed_joint_degree_graph(in_degrees, out_degrees, nkk)
    >>>
    """
    if not is_valid_directed_joint_degree(in_degrees, out_degrees, nkk):
        msg = "Input is not realizable as a simple graph"
        raise nx.NetworkXError(msg)

    # start with an empty directed graph.
    G = nx.DiGraph()

    # for a given group, keep the list of all node ids.
    h_degree_nodelist_in = {}
    h_degree_nodelist_out = {}
    # for a given group, keep the list of all unsaturated node ids.
    h_degree_nodelist_in_unsat = {}
    h_degree_nodelist_out_unsat = {}
    # for a given node, keep track of the remaining stubs to be added.
    h_node_residual_out = {}
    h_node_residual_in = {}
    # for a given node, keep track of the partition id.
    h_partition_out = {}
    h_partition_in = {}
    # keep track of non-chords between pairs of partition ids.
    non_chords = {}

    # populate data structures
    for idx, i in enumerate(in_degrees):
        idx = int(idx)
        if i > 0:
            h_degree_nodelist_in.setdefault(i, [])
            h_degree_nodelist_in_unsat.setdefault(i, set())
            h_degree_nodelist_in[i].append(idx)
            h_degree_nodelist_in_unsat[i].add(idx)
            h_node_residual_in[idx] = i
            h_partition_in[idx] = i

    for idx, o in enumerate(out_degrees):
        o = out_degrees[idx]
        non_chords[(o, in_degrees[idx])] = non_chords.get((o, in_degrees[idx]), 0) + 1
        idx = int(idx)
        if o > 0:
            h_degree_nodelist_out.setdefault(o, [])
            h_degree_nodelist_out_unsat.setdefault(o, set())
            h_degree_nodelist_out[o].append(idx)
            h_degree_nodelist_out_unsat[o].add(idx)
            h_node_residual_out[idx] = o
            h_partition_out[idx] = o

        G.add_node(idx)

    nk_in = {}
    nk_out = {}
    for p in h_degree_nodelist_in:
        nk_in[p] = len(h_degree_nodelist_in[p])
    for p in h_degree_nodelist_out:
        nk_out[p] = len(h_degree_nodelist_out[p])

    # iterate over every degree pair (k,l) and add the number of edges given
    # for each pair.
    for k in nkk:
        for l in nkk[k]:
            n_edges_add = nkk[k][l]

            if n_edges_add > 0:
                # chords contains a random set of potential edges.
                chords = set()

                k_len = nk_out[k]
                l_len = nk_in[l]
                chords_sample = seed.sample(
                    range(k_len * l_len), n_edges_add + non_chords.get((k, l), 0)
                )

                num = 0
                while len(chords) < n_edges_add:
                    i = h_degree_nodelist_out[k][chords_sample[num] % k_len]
                    j = h_degree_nodelist_in[l][chords_sample[num] // k_len]
                    num += 1
                    if i != j:
                        chords.add((i, j))

                # k_unsat and l_unsat consist of nodes of in/out degree k and l
                # that are unsaturated i.e. those nodes that have at least one
                # available stub
                k_unsat = h_degree_nodelist_out_unsat[k]
                l_unsat = h_degree_nodelist_in_unsat[l]

                while n_edges_add > 0:
                    v, w = chords.pop()
                    chords.add((v, w))

                    # if node v has no free stubs then do neighbor switch.
                    if h_node_residual_out[v] == 0:
                        _v = _directed_neighbor_switch(
                            G,
                            v,
                            k_unsat,
                            h_node_residual_out,
                            chords,
                            h_partition_in,
                            l,
                        )
                        if _v is not None:
                            v = _v

                    # if node w has no free stubs then do neighbor switch.
                    if h_node_residual_in[w] == 0:
                        _w = _directed_neighbor_switch_rev(
                            G,
                            w,
                            l_unsat,
                            h_node_residual_in,
                            chords,
                            h_partition_out,
                            k,
                        )
                        if _w is not None:
                            w = _w

                    # add edge (v,w) and update data structures.
                    G.add_edge(v, w)
                    h_node_residual_out[v] -= 1
                    h_node_residual_in[w] -= 1
                    n_edges_add -= 1
                    chords.discard((v, w))

                    if h_node_residual_out[v] == 0:
                        k_unsat.discard(v)
                    if h_node_residual_in[w] == 0:
                        l_unsat.discard(w)
    return G

