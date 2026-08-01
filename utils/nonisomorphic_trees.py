
def nonisomorphic_trees(order):
    """Generate nonisomorphic trees of specified `order`.

    Parameters
    ----------
    order : int
       order of the desired tree(s)

    Yields
    ------
    `networkx.Graph` instances
       A tree with `order` number of nodes that is not isomorphic to any other
       yielded tree.

    Raises
    ------
    ValueError
       If `order` is negative.

    Examples
    --------
    There are 11 unique (non-isomorphic) trees with 7 nodes.

    >>> n = 7
    >>> nit_list = list(nx.nonisomorphic_trees(n))
    >>> len(nit_list) == nx.number_of_nonisomorphic_trees(n) == 11
    True

    All trees yielded by the generator have the specified order.

    >>> all(len(G) == n for G in nx.nonisomorphic_trees(n))
    True

    Each tree is nonisomorphic to every other tree yielded by the generator.
    >>> seen = []
    >>> for G in nx.nonisomorphic_trees(n):
    ...     assert not any(nx.is_isomorphic(G, H) for H in seen)
    ...     seen.append(G)

    See Also
    --------
    number_of_nonisomorphic_trees
    """
    if order < 0:
        raise ValueError("order must be non-negative")
    if order == 0:
        # Idiom for empty generator, i.e. list(nonisomorphic_trees(0)) == []
        return
        yield
    if order == 1:
        yield nx.empty_graph(1)
        return
    # start at the path graph rooted at its center
    layout = list(range(order // 2 + 1)) + list(range(1, (order + 1) // 2))

    while layout is not None:
        layout = _next_tree(layout)
        if layout is not None:
            yield _layout_to_graph(layout)
            layout = _next_rooted_tree(layout)

