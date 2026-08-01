
def test_annihilate_b():
    i, j, n, m = symbols('i,j,n,m')
    o = B(i)
    assert isinstance(o, AnnihilateBoson)
    o = o.subs(i, j)
    assert o.atoms(Symbol) == {j}
    o = B(0)

