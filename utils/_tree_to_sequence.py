
def _tree_to_sequence(tree: Tuple[Any, ...]) -> PathType:
    """Converts a contraction tree to a contraction path as it has to be
    returned by path optimizers. A contraction tree can either be an int
    (=no contraction) or a tuple containing the terms to be contracted. An
    arbitrary number (>= 1) of terms can be contracted at once. Note that
    contractions are commutative, e.g. (j, k, l) = (k, l, j). Note that in
    general, solutions are not unique.

    Parameters:
        c: Contraction tree

    Returns:
        path: Contraction path

    Examples:
        ```python
        _tree_to_sequence(((1,2),(0,(4,5,3))))
        #> [(1, 2), (1, 2, 3), (0, 2), (0, 1)]
        ```
    """
    # ((1,2),(0,(4,5,3))) --> [(1, 2), (1, 2, 3), (0, 2), (0, 1)]
    #
    # 0     0         0           (1,2)       --> ((1,2),(0,(3,4,5)))
    # 1     3         (1,2)   --> (0,(3,4,5))
    # 2 --> 4     --> (3,4,5)
    # 3     5
    # 4     (1,2)
    # 5
    #
    # this function iterates through the table shown above from right to left;

    if type(tree) == int:  # noqa: E721
        return []

    c: List[Tuple[Any, ...]] = [tree]  # list of remaining contractions (lower part of columns shown above)
    t: List[int] = []  # list of elementary tensors (upper part of columns)
    s: List[Tuple[int, ...]] = []  # resulting contraction sequence

    while len(c) > 0:
        j = c.pop(-1)
        s.insert(0, ())

        for i in sorted([i for i in j if type(i) == int]):  # noqa: E721
            s[0] += (sum(1 for q in t if q < i),)
            t.insert(s[0][-1], i)

        for i_tup in [i_tup for i_tup in j if type(i_tup) != int]:  # noqa: E721
            s[0] += (len(t) + len(c),)
            c.append(i_tup)

    return s

