
def tree_isomorphism(t1, t2):
    """
    Return an isomorphic mapping between two trees `t1` and `t2`.

    If `t1` and `t2` are not isomorphic, an empty list is returned.
    Note that two trees may have more than one isomorphism, and this routine just
    returns one valid mapping.

    Parameters
    ----------
    t1 : undirected NetworkX graph
        One of the trees being compared

    t2 : undirected NetworkX graph
        The other tree being compared

    Returns
    -------
    isomorphism : list
        A list of pairs in which the left element is a node in `t1`
        and the right element is a node in `t2`.  The pairs are in
        arbitrary order.  If the nodes in one tree is mapped to the names in
        the other, then trees will be identical. Note that an isomorphism
        will not necessarily be unique.

        If `t1` and `t2` are not isomorphic, then it returns the empty list.

    Raises
    ------
    NetworkXError
        If either `t1` or `t2` is not a tree

    Notes
    -----
    This runs in ``O(n*log(n))`` time for trees with ``n`` nodes.
    """
    if not nx.is_tree(t1):
        raise nx.NetworkXError("t1 is not a tree")
    if not nx.is_tree(t2):
        raise nx.NetworkXError("t2 is not a tree")

    # To be isomorphic, t1 and t2 must have the same number of nodes and sorted
    # degree sequences
    if not nx.faster_could_be_isomorphic(t1, t2):
        return []

    # A tree can have either 1 or 2 centers.
    # If the number doesn't match then t1 and t2 are not isomorphic.
    center1 = nx.center(t1)
    center2 = nx.center(t2)

    if len(center1) != len(center2):
        return []

    # If there is only 1 center in each, then use it.
    if len(center1) == 1:
        return rooted_tree_isomorphism(t1, center1[0], t2, center2[0])

    # If there both have 2 centers,  then try the first for t1
    # with the first for t2.
    attempts = rooted_tree_isomorphism(t1, center1[0], t2, center2[0])

    # If that worked we're done.
    if len(attempts) > 0:
        return attempts

    # Otherwise, try center1[0] with the center2[1], and see if that works
    return rooted_tree_isomorphism(t1, center1[0], t2, center2[1])

