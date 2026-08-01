
def _strongly_connected_components(M):
    """Returns the list of strongly connected vertices of the graph when
    a square matrix is viewed as a weighted graph.

    Examples
    ========

    >>> from sympy import Matrix
    >>> A = Matrix([
    ...     [44, 0, 0, 0, 43, 0, 45, 0, 0],
    ...     [0, 66, 62, 61, 0, 68, 0, 60, 67],
    ...     [0, 0, 22, 21, 0, 0, 0, 20, 0],
    ...     [0, 0, 12, 11, 0, 0, 0, 10, 0],
    ...     [34, 0, 0, 0, 33, 0, 35, 0, 0],
    ...     [0, 86, 82, 81, 0, 88, 0, 80, 87],
    ...     [54, 0, 0, 0, 53, 0, 55, 0, 0],
    ...     [0, 0, 2, 1, 0, 0, 0, 0, 0],
    ...     [0, 76, 72, 71, 0, 78, 0, 70, 77]])
    >>> A.strongly_connected_components()
    [[0, 4, 6], [2, 3, 7], [1, 5, 8]]
    """
    if not M.is_square:
        raise NonSquareMatrixError

    # RepMatrix uses the more efficient DomainMatrix.scc() method
    rep = getattr(M, '_rep', None)
    if rep is not None:
        return rep.scc()

    V = range(M.rows)
    E = sorted(M.todok().keys())
    return strongly_connected_components((V, E))


def _strongly_connected_components(V, Gmap):
    """More efficient internal routine for strongly_connected_components"""
    #
    # Here V is an iterable of vertices and Gmap is a dict mapping each vertex
    # to a list of neighbours e.g.:
    #
    #   V = [0, 1, 2, 3]
    #   Gmap = {0: [2, 3], 1: [0]}
    #
    # For a large graph these data structures can often be created more
    # efficiently then those expected by strongly_connected_components() which
    # in this case would be
    #
    #   V = [0, 1, 2, 3]
    #   Gmap = [(0, 2), (0, 3), (1, 0)]
    #
    # XXX: Maybe this should be the recommended function to use instead...
    #

    # Non-recursive Tarjan's algorithm:
    lowlink = {}
    indices = {}
    stack = OrderedDict()
    callstack = []
    components = []
    nomore = object()

    def start(v):
        index = len(stack)
        indices[v] = lowlink[v] = index
        stack[v] = None
        callstack.append((v, iter(Gmap[v])))

    def finish(v1):
        # Finished a component?
        if lowlink[v1] == indices[v1]:
            component = [stack.popitem()[0]]
            while component[-1] is not v1:
                component.append(stack.popitem()[0])
            components.append(component[::-1])
        v2, _ = callstack.pop()
        if callstack:
            v1, _ = callstack[-1]
            lowlink[v1] = min(lowlink[v1], lowlink[v2])

    for v in V:
        if v in indices:
            continue
        start(v)
        while callstack:
            v1, it1 = callstack[-1]
            v2 = next(it1, nomore)
            # Finished children of v1?
            if v2 is nomore:
                finish(v1)
            # Recurse on v2
            elif v2 not in indices:
                start(v2)
            elif v2 in stack:
                lowlink[v1] = min(lowlink[v1], indices[v2])

    # Reverse topological sort order:
    return components

