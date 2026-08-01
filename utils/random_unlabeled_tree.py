
def random_unlabeled_tree(n, *, number_of_trees=None, seed=None):
    """Returns a tree or list of trees chosen randomly.

    Returns one or more (depending on `number_of_trees`)
    unlabeled trees with `n` nodes drawn uniformly at random.

    Parameters
    ----------
    n : int
        The number of nodes
    number_of_trees : int or None (default)
        If not None, this number of trees is generated and returned.
    seed : integer, random_state, or None (default)
        Indicator of random number generation state.
        See :ref:`Randomness<randomness>`.

    Returns
    -------
    :class:`networkx.Graph` or list of :class:`networkx.Graph`
        A single `networkx.Graph` (or a list thereof, if
        `number_of_trees` is specified) with nodes in the set {0, …, *n* - 1}.

    Raises
    ------
    NetworkXPointlessConcept
        If `n` is zero (because the null graph is not a tree).

    Notes
    -----
    This function generates an unlabeled tree uniformly at random using
    Wilf's algorithm "Free" of [1]_. The algorithm needs to
    compute some counting functions that are relatively expensive:
    in case several trees are needed, it is advisable to use the
    `number_of_trees` optional argument to reuse the counting
    functions.

    References
    ----------
    .. [1] Wilf, Herbert S. "The uniform selection of free trees."
        Journal of Algorithms 2.2 (1981): 204-207.
        https://doi.org/10.1016/0196-6774(81)90021-3
    """
    if n == 0:
        raise nx.NetworkXPointlessConcept("the null graph is not a tree")

    cache_trees = [0, 1]  # initial cache of number of rooted trees
    cache_forests = [1]  # initial cache of number of rooted forests
    if number_of_trees is None:
        return _to_nx(*_random_unlabeled_tree(n, cache_trees, cache_forests, seed))
    else:
        return [
            _to_nx(*_random_unlabeled_tree(n, cache_trees, cache_forests, seed))
            for i in range(number_of_trees)
        ]

