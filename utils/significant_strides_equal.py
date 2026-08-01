
def significant_strides_equal(
    strides1: Sequence[_IntLike],
    strides2: Sequence[_IntLike],
    shape: Sequence[_IntLike],
) -> bool:
    """
    Returns true if the strides are equal, ignoring dimensions of size 1 .
    """
    assert len(shape) == len(strides1) and len(strides1) == len(strides2)
    for dim, s1, s2 in zip(shape, strides1, strides2):
        if V.graph.sizevars.statically_known_leq(dim, 1):
            continue

        if not V.graph.sizevars.guard_or_false(sympy.Eq(s1, s2)):
            return False
    return True

