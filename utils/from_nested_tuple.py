
def from_nested_tuple(sequence, sensible_relabeling=False):
    """Returns the rooted tree corresponding to the given nested tuple.

    The nested tuple representation of a tree is defined
    recursively. The tree with one node and no edges is represented by
    the empty tuple, ``()``. A tree with ``k`` subtrees is represented
    by a tuple of length ``k`` in which each element is the nested tuple
    representation of a subtree.

    Parameters
    ----------
    sequence : tuple
        A nested tuple representing a rooted tree.

    sensible_relabeling : bool
        Whether to relabel the nodes of the tree so that nodes are
        labeled in increasing order according to their breadth-first
        search order from the root node.

    Returns
    -------
    NetworkX graph
        The tree corresponding to the given nested tuple, whose root
        node is node 0. If ``sensible_labeling`` is ``True``, nodes will
        be labeled in breadth-first search order starting from the root
        node.

    Notes
    -----
    This function is *not* the inverse of :func:`to_nested_tuple`; the
    only guarantee is that the rooted trees are isomorphic.

    See also
    --------
    to_nested_tuple
    from_prufer_sequence

    Examples
    --------
    Sensible relabeling ensures that the nodes are labeled from the root
    starting at 0::

        >>> balanced = (((), ()), ((), ()))
        >>> T = nx.from_nested_tuple(balanced, sensible_relabeling=True)
        >>> edges = [(0, 1), (0, 2), (1, 3), (1, 4), (2, 5), (2, 6)]
        >>> all((u, v) in T.edges() or (v, u) in T.edges() for (u, v) in edges)
        True

    """

    def _make_tree(sequence):
        """Recursively creates a tree from the given sequence of nested
        tuples.

        This function employs the :func:`~networkx.tree.join` function
        to recursively join subtrees into a larger tree.

        """
        # The empty sequence represents the empty tree, which is the
        # (unique) graph with a single node. We mark the single node
        # with an attribute that indicates that it is the root of the
        # graph.
        if len(sequence) == 0:
            return nx.empty_graph(1)
        # For a nonempty sequence, get the subtrees for each child
        # sequence and join all the subtrees at their roots. After
        # joining the subtrees, the root is node 0.
        return nx.tree.join_trees([(_make_tree(child), 0) for child in sequence])

    # Make the tree and remove the `is_root` node attribute added by the
    # helper function.
    T = _make_tree(sequence)
    if sensible_relabeling:
        # Relabel the nodes according to their breadth-first search
        # order, starting from the root node (that is, the node 0).
        bfs_nodes = chain([0], (v for u, v in nx.bfs_edges(T, 0)))
        labels = {v: i for i, v in enumerate(bfs_nodes)}
        # We would like to use `copy=False`, but `relabel_nodes` doesn't
        # allow a relabel mapping that can't be topologically sorted.
        T = nx.relabel_nodes(T, labels)
    return T

