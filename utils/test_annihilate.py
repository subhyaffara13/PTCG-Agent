
def test_annihilate():
    i, j, n, m, p1 = symbols('i,j,n,m,p1')
    o = B(i)
    assert latex(o) == "b_{i}"
    assert latex(B(p1)) == "b_{p_{1}}"
    assert isinstance(o, AnnihilateBoson)
    o = o.subs(i, j)
    assert o.atoms(Symbol) == {j}
    o = B(0)
    assert o.apply_operator(BKet([n])) == sqrt(n)*BKet([n - 1])
    o = B(n)
    assert o.apply_operator(BKet([n])) == o*BKet([n])

