
def test_create(num_elems):
    vo = m.VectorOwner.Create(num_elems)
    assert vo.data_size() == num_elems


def test_create():
    i, j, n, m, p1 = symbols('i,j,n,m,p1')
    o = Bd(i)
    assert latex(o) == "{b^\\dagger_{i}}"
    assert latex(Bd(p1)) == "{b^\\dagger_{p_{1}}}"
    assert isinstance(o, CreateBoson)
    o = o.subs(i, j)
    assert o.atoms(Symbol) == {j}
    o = Bd(0)
    assert o.apply_operator(BKet([n])) == sqrt(n + 1)*BKet([n + 1])
    o = Bd(n)
    assert o.apply_operator(BKet([n])) == o*BKet([n])

