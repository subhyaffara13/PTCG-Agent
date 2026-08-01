
def number_of_nonisomorphic_trees(order):
    """Returns the number of nonisomorphic trees of the specified `order`.

    Based on an algorithm by Alois P. Heinz in
    `OEIS entry A000055 <https://oeis.org/A000055>`_. Complexity is ``O(n ** 3)``.

    Parameters
    ----------
    order : int
       Order of the desired tree(s).

    Returns
    -------
    int
       Number of nonisomorphic trees with `order` number of nodes.

    Raises
    ------
    ValueError
       If `order` is negative.

    Examples
    --------
    >>> nx.number_of_nonisomorphic_trees(10)
    106

    See Also
    --------
    nonisomorphic_trees
    """
    if order < 0:
        raise ValueError("order must be non-negative")
    return _unlabeled_trees(order)

