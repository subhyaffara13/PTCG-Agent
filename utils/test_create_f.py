
def test_create_f():
    i, j, n, m = symbols('i,j,n,m')
    o = Fd(i)
    assert isinstance(o, CreateFermion)
    o = o.subs(i, j)
    assert o.atoms(Symbol) == {j}
    o = Fd(1)
    assert o.apply_operator(FKet([n])) == FKet([1, n])
    assert o.apply_operator(FKet([n])) == -FKet([n, 1])
    o = Fd(n)
    assert o.apply_operator(FKet([])) == FKet([n])

    vacuum = FKet([], fermi_level=4)
    assert vacuum == FKet([], fermi_level=4)

    i, j, k, l = symbols('i,j,k,l', below_fermi=True)
    a, b, c, d = symbols('a,b,c,d', above_fermi=True)
    p, q, r, s = symbols('p,q,r,s')
    p1 = symbols("p1")

    assert Fd(i).apply_operator(FKet([i, j, k], 4)) == FKet([j, k], 4)
    assert Fd(a).apply_operator(FKet([i, b, k], 4)) == FKet([a, i, b, k], 4)

    assert Dagger(B(p)).apply_operator(q) == q*CreateBoson(p)
    assert repr(Fd(p)) == 'CreateFermion(p)'
    assert srepr(Fd(p)) == "CreateFermion(Symbol('p'))"
    assert latex(Fd(p)) == r'{a^\dagger_{p}}'
    assert latex(Fd(p1)) == r'{a^\dagger_{p_{1}}}'
    assert latex(FKet([a,i], 1)) == r"\left|\left( a, \  i\right)\right\rangle"
    assert latex(FKet([j,i,b,a], 2)) == r"\left|\left( a, \  b, \  i, \  j\right)\right\rangle"

