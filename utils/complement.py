
def complement(func):
    """ Convert a predicate function to its logical complement.

    In other words, return a function that, for inputs that normally
    yield True, yields False, and vice-versa.

    >>> def iseven(n): return n % 2 == 0
    >>> isodd = complement(iseven)
    >>> iseven(2)
    True
    >>> isodd(2)
    False
    """
    return compose(not_, func)


def complement(layout: LayoutOrIntTuple, max_idx: int = 1) -> Layout:
    if is_int(layout):
        return complement(Layout(layout))

    result_shape = []
    result_stride = []
    current_idx = 1

    sorted_DS = sorted(zip(flatten(layout.stride), flatten(layout.shape)))  # type: ignore[union-attr]
    for stride, shape in sorted_DS:
        if stride == 0 or shape == 1:
            continue

        in_bound = current_idx <= shape * stride
        # To support symbolic value which can't be evaluated now
        if (type(in_bound) is bool) and not in_bound:
            raise AssertionError

        result_shape.append(stride // current_idx)
        result_stride.append(current_idx)
        current_idx = shape * stride

    result_shape.append((max_idx + current_idx - 1) // current_idx)  # ceil_div
    result_stride.append(current_idx)
    # This is different from original pycute implementation, because we want to follow the lexicographic order here
    # where the right-most dimension is the innermost dimension (smallest stride).
    result_shape.reverse()
    result_stride.reverse()

    return coalesce(Layout(tuple(result_shape), tuple(result_stride)))


def complement(G):
    """Returns the graph complement of G.

    Parameters
    ----------
    G : graph
       A NetworkX graph

    Returns
    -------
    GC : A new graph.

    Notes
    -----
    Note that `complement` does not create self-loops and also
    does not produce parallel edges for MultiGraphs.

    Graph, node, and edge data are not propagated to the new graph.

    Examples
    --------
    >>> G = nx.Graph([(1, 2), (1, 3), (2, 3), (3, 4), (3, 5)])
    >>> G_complement = nx.complement(G)
    >>> G_complement.edges()  # This shows the edges of the complemented graph
    EdgeView([(1, 4), (1, 5), (2, 4), (2, 5), (4, 5)])

    """
    R = G.__class__()
    R.add_nodes_from(G)
    R.add_edges_from(
        ((n, n2) for n, nbrs in G.adjacency() for n2 in G if n2 not in nbrs if n != n2)
    )
    return R

