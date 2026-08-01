
def transitive_closure(
    tvars: list[TypeVarId], constraints: list[Constraint]
) -> tuple[Graph, Bounds, Bounds]:
    """Find transitive closure for given constraints on type variables.

    Transitive closure gives maximal set of lower/upper bounds for each type variable,
    such that we cannot deduce any further bounds by chaining other existing bounds.

    The transitive closure is represented by:
      * A set of lower and upper bounds for each type variable, where only constant and
        non-linear terms are included in the bounds.
      * A graph of linear constraints between type variables (represented as a set of pairs)
    Such separation simplifies reasoning, and allows an efficient and simple incremental
    transitive closure algorithm that we use here.

    For example if we have initial constraints [T <: S, S <: U, U <: int], the transitive
    closure is given by:
      * {} <: T <: {int}
      * {} <: S <: {int}
      * {} <: U <: {int}
      * {T <: S, S <: U, T <: U}
    """
    uppers: Bounds = defaultdict(set)
    lowers: Bounds = defaultdict(set)
    graph: Graph = {(tv, tv) for tv in tvars}

    remaining = set(constraints)
    while remaining:
        c = remaining.pop()
        # Note that ParamSpec constraint P <: Q may be considered linear only if Q has no prefix,
        # for cases like P <: Concatenate[T, Q] we should consider this non-linear and put {P} and
        # {T, Q} into separate SCCs. Similarly, Ts <: Tuple[*Us] considered linear, while
        # Ts <: Tuple[*Us, U] is non-linear.
        is_linear, target_id = find_linear(c)
        if is_linear and target_id in tvars:
            assert target_id is not None
            if c.op == SUBTYPE_OF:
                lower, upper = c.type_var, target_id
            else:
                lower, upper = target_id, c.type_var
            if (lower, upper) in graph:
                continue
            graph |= {
                (l, u) for l in tvars for u in tvars if (l, lower) in graph and (upper, u) in graph
            }
            for u in tvars:
                if (upper, u) in graph:
                    lowers[u] |= lowers[lower]
            for l in tvars:
                if (l, lower) in graph:
                    uppers[l] |= uppers[upper]
            for lt in lowers[lower]:
                for ut in uppers[upper]:
                    add_secondary_constraints(remaining, lt, ut)
        elif c.op == SUBTYPE_OF:
            if c.target in uppers[c.type_var]:
                continue
            for l in tvars:
                if (l, c.type_var) in graph:
                    uppers[l].add(c.target)
            for lt in lowers[c.type_var]:
                add_secondary_constraints(remaining, lt, c.target)
        else:
            assert c.op == SUPERTYPE_OF
            if c.target in lowers[c.type_var]:
                continue
            for u in tvars:
                if (c.type_var, u) in graph:
                    lowers[u].add(c.target)
            for ut in uppers[c.type_var]:
                add_secondary_constraints(remaining, c.target, ut)
    return graph, lowers, uppers


def transitive_closure(implications):
    """
    Computes the transitive closure of a list of implications

    Uses Warshall's algorithm, as described at
    http://www.cs.hope.edu/~cusack/Notes/Notes/DiscreteMath/Warshall.pdf.
    """
    full_implications = set(implications)
    literals = set().union(*map(set, full_implications))

    for k in literals:
        for i in literals:
            if (i, k) in full_implications:
                for j in literals:
                    if (k, j) in full_implications:
                        full_implications.add((i, j))

    return full_implications


def transitive_closure(G, reflexive=False):
    """Returns transitive closure of a graph

    The transitive closure of G = (V,E) is a graph G+ = (V,E+) such that
    for all v, w in V there is an edge (v, w) in E+ if and only if there
    is a path from v to w in G.

    Handling of paths from v to v has some flexibility within this definition.
    A reflexive transitive closure creates a self-loop for the path
    from v to v of length 0. The usual transitive closure creates a
    self-loop only if a cycle exists (a path from v to v with length > 0).
    We also allow an option for no self-loops.

    Parameters
    ----------
    G : NetworkX Graph
        A directed/undirected graph/multigraph.
    reflexive : Bool or None, optional (default: False)
        Determines when cycles create self-loops in the Transitive Closure.
        If True, trivial cycles (length 0) create self-loops. The result
        is a reflexive transitive closure of G.
        If False (the default) non-trivial cycles create self-loops.
        If None, self-loops are not created.

    Returns
    -------
    NetworkX graph
        The transitive closure of `G`

    Raises
    ------
    NetworkXError
        If `reflexive` not in `{None, True, False}`

    Examples
    --------
    The treatment of trivial (i.e. length 0) cycles is controlled by the
    `reflexive` parameter.

    Trivial (i.e. length 0) cycles do not create self-loops when
    ``reflexive=False`` (the default)::

        >>> DG = nx.DiGraph([(1, 2), (2, 3)])
        >>> TC = nx.transitive_closure(DG, reflexive=False)
        >>> TC.edges()
        OutEdgeView([(1, 2), (1, 3), (2, 3)])

    However, nontrivial (i.e. length greater than 0) cycles create self-loops
    when ``reflexive=False`` (the default)::

        >>> DG = nx.DiGraph([(1, 2), (2, 3), (3, 1)])
        >>> TC = nx.transitive_closure(DG, reflexive=False)
        >>> TC.edges()
        OutEdgeView([(1, 2), (1, 3), (1, 1), (2, 3), (2, 1), (2, 2), (3, 1), (3, 2), (3, 3)])

    Trivial cycles (length 0) create self-loops when ``reflexive=True``::

        >>> DG = nx.DiGraph([(1, 2), (2, 3)])
        >>> TC = nx.transitive_closure(DG, reflexive=True)
        >>> TC.edges()
        OutEdgeView([(1, 2), (1, 1), (1, 3), (2, 3), (2, 2), (3, 3)])

    And the third option is not to create self-loops at all when ``reflexive=None``::

        >>> DG = nx.DiGraph([(1, 2), (2, 3), (3, 1)])
        >>> TC = nx.transitive_closure(DG, reflexive=None)
        >>> TC.edges()
        OutEdgeView([(1, 2), (1, 3), (2, 3), (2, 1), (3, 1), (3, 2)])

    References
    ----------
    .. [1] https://www.ics.uci.edu/~eppstein/PADS/PartialOrder.py
    """
    TC = G.copy()

    if reflexive not in {None, True, False}:
        raise nx.NetworkXError("Incorrect value for the parameter `reflexive`")

    for v in G:
        if reflexive is None:
            TC.add_edges_from((v, u) for u in nx.descendants(G, v) if u not in TC[v])
        elif reflexive is True:
            TC.add_edges_from(
                (v, u) for u in nx.descendants(G, v) | {v} if u not in TC[v]
            )
        elif reflexive is False:
            TC.add_edges_from((v, e[1]) for e in nx.edge_bfs(G, v) if e[1] not in TC[v])

    return TC

