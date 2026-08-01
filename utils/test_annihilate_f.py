
def test_annihilate_f():
    i, j, n, m = symbols('i,j,n,m')
    o = F(i)
    assert isinstance(o, AnnihilateFermion)
    o = o.subs(i, j)
    assert o.atoms(Symbol) == {j}
    o = F(1)
    assert o.apply_operator(FKet([1, n])) == FKet([n])
    assert o.apply_operator(FKet([n, 1])) == -FKet([n])
    o = F(n)
    assert o.apply_operator(FKet([n])) == FKet([])

    i, j, k, l = symbols('i,j,k,l', below_fermi=True)
    a, b, c, d = symbols('a,b,c,d', above_fermi=True)
    p, q, r, s = symbols('p,q,r,s')
    p1 = symbols('p1')

    assert F(i).apply_operator(FKet([i, j, k], 4)) == 0
    assert F(a).apply_operator(FKet([i, b, k], 4)) == 0
    assert F(l).apply_operator(FKet([i, j, k], 3)) == 0
    assert F(l).apply_operator(FKet([i, j, k], 4)) == FKet([l, i, j, k], 4)
    assert str(F(p)) == 'f(p)'
    assert repr(F(p)) == 'AnnihilateFermion(p)'
    assert srepr(F(p)) == "AnnihilateFermion(Symbol('p'))"
    assert latex(F(p)) == 'a_{p}'
    assert latex(F(p1)) == 'a_{p_{1}}'

