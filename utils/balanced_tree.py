
def balanced_tree(r, h, create_using=None):
    """Returns the perfectly balanced `r`-ary tree of height `h`.

    .. plot::

        >>> nx.draw(nx.balanced_tree(2, 3))

    Parameters
    ----------
    r : int
        Branching factor of the tree; each node will have `r`
        children.

    h : int
        Height of the tree.

    create_using : NetworkX graph constructor, optional (default=nx.Graph)
       Graph type to create. If graph instance, then cleared before populated.

    Returns
    -------
    G : NetworkX graph
        A balanced `r`-ary tree of height `h`.

    Notes
    -----
    This is the rooted tree where all leaves are at distance `h` from
    the root. The root has degree `r` and all other internal nodes
    have degree `r + 1`.

    Node labels are integers, starting from zero.

    A balanced tree is also known as a *complete r-ary tree*.

    """
    # The number of nodes in the balanced tree is `1 + r + ... + r^h`,
    # which is computed by using the closed-form formula for a geometric
    # sum with ratio `r`. In the special case that `r` is 1, the number
    # of nodes is simply `h + 1` (since the tree is actually a path
    # graph).
    if r == 1:
        n = h + 1
    else:
        # This must be an integer if both `r` and `h` are integers. If
        # they are not, we force integer division anyway.
        n = (1 - r ** (h + 1)) // (1 - r)
    return full_rary_tree(r, n, create_using=create_using)

