
def test_equivalent_internal_lines_VT2_AT():
    i, j, k, l = symbols('i j k l', below_fermi=True, cls=Dummy)
    a, b, c, d = symbols('a b c d', above_fermi=True, cls=Dummy)

    exprs = [
        # permute v. Same dummy order, not equivalent.
        atv(i, j, a, b)*att(a, b, i, j),
        atv(j, i, a, b)*att(a, b, i, j),
        atv(i, j, b, a)*att(a, b, i, j),
    ]
    for permut in exprs[1:]:
        assert substitute_dummies(exprs[0]) != substitute_dummies(permut)

    exprs = [
        # permute t.
        atv(i, j, a, b)*att(a, b, i, j),
        atv(i, j, a, b)*att(b, a, i, j),
        atv(i, j, a, b)*att(a, b, j, i),
    ]
    for permut in exprs[1:]:
        assert substitute_dummies(exprs[0]) != substitute_dummies(permut)

    exprs = [  # permute v and t.  Relabelling of dummies should be equivalent.
        atv(i, j, a, b)*att(a, b, i, j),
        atv(j, i, a, b)*att(a, b, j, i),
        atv(i, j, b, a)*att(b, a, i, j),
        atv(j, i, b, a)*att(b, a, j, i),
    ]
    for permut in exprs[1:]:
        assert substitute_dummies(exprs[0]) == substitute_dummies(permut)

