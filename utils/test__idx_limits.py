
def test_Idx_limits():
    i = symbols('i', cls=Idx)
    r = Indexed('r', i)

    assert SeqFormula(r, (i, 0, 5))[:] == [r.subs(i, j) for j in range(6)]
    assert SeqPer((1, 2), (i, 0, 5))[:] == [1, 2, 1, 2, 1, 2]

