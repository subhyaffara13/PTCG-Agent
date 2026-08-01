
def _greedy_modularity_communities_generator(G, weight=None, resolution=1):
    r"""Yield community partitions of G and the modularity change at each step.

    This function performs Clauset-Newman-Moore greedy modularity maximization [2]_
    At each step of the process it yields the change in modularity that will occur in
    the next step followed by yielding the new community partition after that step.

    Greedy modularity maximization begins with each node in its own community
    and repeatedly joins the pair of communities that lead to the largest
    modularity until one community contains all nodes (the partition has one set).

    This function maximizes the generalized modularity, where `resolution`
    is the resolution parameter, often expressed as $\gamma$.
    See :func:`~networkx.algorithms.community.quality.modularity`.

    Parameters
    ----------
    G : NetworkX graph

    weight : string or None, optional (default=None)
        The name of an edge attribute that holds the numerical value used
        as a weight.  If None, then each edge has weight 1.
        The degree is the sum of the edge weights adjacent to the node.

    resolution : float (default=1)
        If resolution is less than 1, modularity favors larger communities.
        Greater than 1 favors smaller communities.

    Yields
    ------
    Alternating yield statements produce the following two objects:

    communities: dict_values
        A dict_values of frozensets of nodes, one for each community.
        This represents a partition of the nodes of the graph into communities.
        The first yield is the partition with each node in its own community.

    dq: float
        The change in modularity when merging the next two communities
        that leads to the largest modularity.

    See Also
    --------
    modularity

    References
    ----------
    .. [1] Newman, M. E. J. "Networks: An Introduction", page 224
       Oxford University Press 2011.
    .. [2] Clauset, A., Newman, M. E., & Moore, C.
       "Finding community structure in very large networks."
       Physical Review E 70(6), 2004.
    .. [3] Reichardt and Bornholdt "Statistical Mechanics of Community
       Detection" Phys. Rev. E74, 2006.
    .. [4] Newman, M. E. J."Analysis of weighted networks"
       Physical Review E 70(5 Pt 2):056131, 2004.
    """
    directed = G.is_directed()
    N = G.number_of_nodes()

    # Count edges (or the sum of edge-weights for weighted graphs)
    m = G.size(weight)
    q0 = 1 / m

    # Calculate degrees (notation from the papers)
    # a : the fraction of (weighted) out-degree for each node
    # b : the fraction of (weighted) in-degree for each node
    if directed:
        a = {node: deg_out * q0 for node, deg_out in G.out_degree(weight=weight)}
        b = {node: deg_in * q0 for node, deg_in in G.in_degree(weight=weight)}
    else:
        a = b = {node: deg * q0 * 0.5 for node, deg in G.degree(weight=weight)}

    # this preliminary step collects the edge weights for each node pair
    # It handles multigraph and digraph and works fine for graph.
    dq_dict = defaultdict(lambda: defaultdict(float))
    for u, v, wt in G.edges(data=weight, default=1):
        if u == v:
            continue
        dq_dict[u][v] += wt
        dq_dict[v][u] += wt

    # now scale and subtract the expected edge-weights term
    for u, nbrdict in dq_dict.items():
        for v, wt in nbrdict.items():
            dq_dict[u][v] = q0 * wt - resolution * (a[u] * b[v] + b[u] * a[v])

    # Use -dq to get a max_heap instead of a min_heap
    # dq_heap holds a heap for each node's neighbors
    dq_heap = {u: MappedQueue({(u, v): -dq for v, dq in dq_dict[u].items()}) for u in G}
    # H -> all_dq_heap holds a heap with the best items for each node
    H = MappedQueue([dq_heap[n].heap[0] for n in G if len(dq_heap[n]) > 0])

    # Initialize single-node communities
    communities = {n: frozenset([n]) for n in G}
    yield communities.values()

    # Merge the two communities that lead to the largest modularity
    while len(H) > 1:
        # Find best merge
        # Remove from heap of row maxes
        # Ties will be broken by choosing the pair with lowest min community id
        try:
            negdq, u, v = H.pop()
        except IndexError:
            break
        dq = -negdq
        yield dq
        # Remove best merge from row u heap
        dq_heap[u].pop()
        # Push new row max onto H
        if len(dq_heap[u]) > 0:
            H.push(dq_heap[u].heap[0])
        # If this element was also at the root of row v, we need to remove the
        # duplicate entry from H
        if dq_heap[v].heap[0] == (v, u):
            H.remove((v, u))
            # Remove best merge from row v heap
            dq_heap[v].remove((v, u))
            # Push new row max onto H
            if len(dq_heap[v]) > 0:
                H.push(dq_heap[v].heap[0])
        else:
            # Duplicate wasn't in H, just remove from row v heap
            dq_heap[v].remove((v, u))

        # Perform merge
        communities[v] = frozenset(communities[u] | communities[v])
        del communities[u]

        # Get neighbor communities connected to the merged communities
        u_nbrs = set(dq_dict[u])
        v_nbrs = set(dq_dict[v])
        all_nbrs = (u_nbrs | v_nbrs) - {u, v}
        both_nbrs = u_nbrs & v_nbrs
        # Update dq for merge of u into v
        for w in all_nbrs:
            # Calculate new dq value
            if w in both_nbrs:
                dq_vw = dq_dict[v][w] + dq_dict[u][w]
            elif w in v_nbrs:
                dq_vw = dq_dict[v][w] - resolution * (a[u] * b[w] + a[w] * b[u])
            else:  # w in u_nbrs
                dq_vw = dq_dict[u][w] - resolution * (a[v] * b[w] + a[w] * b[v])
            # Update rows v and w
            for row, col in [(v, w), (w, v)]:
                dq_heap_row = dq_heap[row]
                # Update dict for v,w only (u is removed below)
                dq_dict[row][col] = dq_vw
                # Save old max of per-row heap
                if len(dq_heap_row) > 0:
                    d_oldmax = dq_heap_row.heap[0]
                else:
                    d_oldmax = None
                # Add/update heaps
                d = (row, col)
                d_negdq = -dq_vw
                # Save old value for finding heap index
                if w in v_nbrs:
                    # Update existing element in per-row heap
                    dq_heap_row.update(d, d, priority=d_negdq)
                else:
                    # We're creating a new nonzero element, add to heap
                    dq_heap_row.push(d, priority=d_negdq)
                # Update heap of row maxes if necessary
                if d_oldmax is None:
                    # No entries previously in this row, push new max
                    H.push(d, priority=d_negdq)
                else:
                    # We've updated an entry in this row, has the max changed?
                    row_max = dq_heap_row.heap[0]
                    if d_oldmax != row_max or d_oldmax.priority != row_max.priority:
                        H.update(d_oldmax, row_max)

        # Remove row/col u from dq_dict matrix
        for w in dq_dict[u]:
            # Remove from dict
            dq_old = dq_dict[w][u]
            del dq_dict[w][u]
            # Remove from heaps if we haven't already
            if w != v:
                # Remove both row and column
                for row, col in [(w, u), (u, w)]:
                    dq_heap_row = dq_heap[row]
                    # Check if replaced dq is row max
                    d_old = (row, col)
                    if dq_heap_row.heap[0] == d_old:
                        # Update per-row heap and heap of row maxes
                        dq_heap_row.remove(d_old)
                        H.remove(d_old)
                        # Update row max
                        if len(dq_heap_row) > 0:
                            H.push(dq_heap_row.heap[0])
                    else:
                        # Only update per-row heap
                        dq_heap_row.remove(d_old)

        del dq_dict[u]
        # Mark row u as deleted, but keep placeholder
        dq_heap[u] = MappedQueue()
        # Merge u into v and update a
        a[v] += a[u]
        a[u] = 0
        if directed:
            b[v] += b[u]
            b[u] = 0

        yield communities.values()

