
def constraint(G, nodes=None, weight=None):
    r"""Returns the constraint on all nodes in the graph ``G``.

    The *constraint* is a measure of the extent to which a node *v* is
    invested in those nodes that are themselves invested in the
    neighbors of *v*. Formally, the *constraint on v*, denoted `c(v)`,
    is defined by

    .. math::

       c(v) = \sum_{w \in N(v) \setminus \{v\}} \ell(v, w)

    where $N(v)$ is the subset of the neighbors of `v` that are either
    predecessors or successors of `v` and $\ell(v, w)$ is the local
    constraint on `v` with respect to `w` [1]_. For the definition of local
    constraint, see :func:`local_constraint`.

    Parameters
    ----------
    G : NetworkX graph
        The graph containing ``v``. This can be either directed or undirected.

    nodes : container, optional
        Container of nodes in the graph ``G`` to compute the constraint. If
        None, the constraint of every node is computed.

    weight : None or string, optional
      If None, all edge weights are considered equal.
      Otherwise holds the name of the edge attribute used as weight.

    Returns
    -------
    dict
        Dictionary with nodes as keys and the constraint on the node as values.

    See also
    --------
    local_constraint

    References
    ----------
    .. [1] Burt, Ronald S.
           "Structural holes and good ideas".
           American Journal of Sociology (110): 349–399.

    """

    # Check if scipy is available
    try:
        # Needed for errstate
        import numpy as np

        # make sure nx.adjacency_matrix will not raise
        import scipy as sp

        has_scipy = True
    except:
        has_scipy = False

    if nodes is None and has_scipy:
        # In order to compute constraint of all nodes,
        # algorithms based on sparse matrices can be much faster

        # Obtain the adjacency matrix
        P = nx.adjacency_matrix(G, weight=weight)

        # Calculate mutual weights
        mutual_weights = P + P.T

        # Normalize mutual weights by row sums
        sum_mutual_weights = mutual_weights.sum(axis=1)
        with np.errstate(divide="ignore"):
            mutual_weights /= sum_mutual_weights[:, np.newaxis]

        # Calculate local constraints and constraints
        local_constraints = (mutual_weights + mutual_weights @ mutual_weights) ** 2
        constraints = ((mutual_weights > 0) * local_constraints).sum(axis=1)

        # Special treatment: isolated nodes marked with "nan"
        isolated_nodes = sum_mutual_weights - 2 * mutual_weights.diagonal() == 0
        constraints[isolated_nodes] = float("nan")
        # Use tolist() to automatically convert numpy scalars -> Python scalars
        return dict(zip(G, constraints.tolist()))

    # Result for only requested nodes
    constraint = {}
    if nodes is None:
        nodes = G
    for v in nodes:
        # Constraint is not defined for isolated nodes
        if len(G[v]) == 0:
            constraint[v] = float("nan")
            continue
        constraint[v] = sum(
            local_constraint(G, v, n, weight) for n in set(nx.all_neighbors(G, v))
        )
    return constraint

