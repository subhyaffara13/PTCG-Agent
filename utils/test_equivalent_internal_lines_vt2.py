
def test_equivalent_internal_lines_VT2():
    i, j, k, l = symbols('i j k l', below_fermi=True, cls=Dummy)
    a, b, c, d = symbols('a b c d', above_fermi=True, cls=Dummy)

    v = Function('v')
    t = Function('t')
    dums = _get_ordered_dummies
    exprs = [
        # permute v. Same dummy order, not equivalent.
        #
        # This test show that the dummy order may not be sensitive to all
        # index permutations.  The following expressions have identical
        # structure as the resulting terms from of the dummy substitutions
        # in the test above.  Here, all expressions have the same dummy
        # order, so they cannot be simplified by means of dummy
        # substitution.  In order to simplify further, it is necessary to
        # exploit symmetries in the objects, for instance if t or v is
        # antisymmetric.
        v(i, j, a, b)*t(a, b, i, j),
        v(j, i, a, b)*t(a, b, i, j),
        v(i, j, b, a)*t(a, b, i, j),
        v(j, i, b, a)*t(a, b, i, j),
    ]
    for permut in exprs[1:]:
        assert dums(exprs[0]) == dums(permut)
        assert substitute_dummies(exprs[0]) != substitute_dummies(permut)

    exprs = [
        # permute t.
        v(i, j, a, b)*t(a, b, i, j),
        v(i, j, a, b)*t(b, a, i, j),
        v(i, j, a, b)*t(a, b, j, i),
        v(i, j, a, b)*t(b, a, j, i),
    ]
    for permut in exprs[1:]:
        assert dums(exprs[0]) != dums(permut)
        assert substitute_dummies(exprs[0]) != substitute_dummies(permut)

    exprs = [  # permute v and t.  Relabelling of dummies should be equivalent.
        v(i, j, a, b)*t(a, b, i, j),
        v(j, i, a, b)*t(a, b, j, i),
        v(i, j, b, a)*t(b, a, i, j),
        v(j, i, b, a)*t(b, a, j, i),
    ]
    for permut in exprs[1:]:
        assert dums(exprs[0]) != dums(permut)
        assert substitute_dummies(exprs[0]) == substitute_dummies(permut)

