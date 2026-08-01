
def test_equivalent_internal_lines_VT1T1():
    i, j, k, l = symbols('i j k l', below_fermi=True, cls=Dummy)
    a, b, c, d = symbols('a b c d', above_fermi=True, cls=Dummy)

    v = Function('v')
    t = Function('t')
    dums = _get_ordered_dummies

    exprs = [  # permute v.  Different dummy order. Not equivalent.
        v(i, j, a, b)*t(a, i)*t(b, j),
        v(j, i, a, b)*t(a, i)*t(b, j),
        v(i, j, b, a)*t(a, i)*t(b, j),
    ]
    for permut in exprs[1:]:
        assert dums(exprs[0]) != dums(permut)
        assert substitute_dummies(exprs[0]) != substitute_dummies(permut)

    exprs = [  # permute v.  Different dummy order. Equivalent
        v(i, j, a, b)*t(a, i)*t(b, j),
        v(j, i, b, a)*t(a, i)*t(b, j),
    ]
    for permut in exprs[1:]:
        assert dums(exprs[0]) != dums(permut)
        assert substitute_dummies(exprs[0]) == substitute_dummies(permut)

    exprs = [  # permute t.  Same dummy order, not equivalent.
        v(i, j, a, b)*t(a, i)*t(b, j),
        v(i, j, a, b)*t(b, i)*t(a, j),
    ]
    for permut in exprs[1:]:
        assert dums(exprs[0]) == dums(permut)
        assert substitute_dummies(exprs[0]) != substitute_dummies(permut)

    exprs = [  # permute v and t.  Different dummy order, equivalent
        v(i, j, a, b)*t(a, i)*t(b, j),
        v(j, i, a, b)*t(a, j)*t(b, i),
        v(i, j, b, a)*t(b, i)*t(a, j),
        v(j, i, b, a)*t(b, j)*t(a, i),
    ]
    for permut in exprs[1:]:
        assert dums(exprs[0]) != dums(permut)
        assert substitute_dummies(exprs[0]) == substitute_dummies(permut)

