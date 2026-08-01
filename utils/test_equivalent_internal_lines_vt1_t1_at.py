
def test_equivalent_internal_lines_VT1T1_AT():
    i, j, k, l = symbols('i j k l', below_fermi=True, cls=Dummy)
    a, b, c, d = symbols('a b c d', above_fermi=True, cls=Dummy)

    exprs = [  # permute v.  Different dummy order. Not equivalent.
        atv(i, j, a, b)*att(a, i)*att(b, j),
        atv(j, i, a, b)*att(a, i)*att(b, j),
        atv(i, j, b, a)*att(a, i)*att(b, j),
    ]
    for permut in exprs[1:]:
        assert substitute_dummies(exprs[0]) != substitute_dummies(permut)

    exprs = [  # permute v.  Different dummy order. Equivalent
        atv(i, j, a, b)*att(a, i)*att(b, j),
        atv(j, i, b, a)*att(a, i)*att(b, j),
    ]
    for permut in exprs[1:]:
        assert substitute_dummies(exprs[0]) == substitute_dummies(permut)

    exprs = [  # permute t.  Same dummy order, not equivalent.
        atv(i, j, a, b)*att(a, i)*att(b, j),
        atv(i, j, a, b)*att(b, i)*att(a, j),
    ]
    for permut in exprs[1:]:
        assert substitute_dummies(exprs[0]) != substitute_dummies(permut)

    exprs = [  # permute v and t.  Different dummy order, equivalent
        atv(i, j, a, b)*att(a, i)*att(b, j),
        atv(j, i, a, b)*att(a, j)*att(b, i),
        atv(i, j, b, a)*att(b, i)*att(a, j),
        atv(j, i, b, a)*att(b, j)*att(a, i),
    ]
    for permut in exprs[1:]:
        assert substitute_dummies(exprs[0]) == substitute_dummies(permut)

