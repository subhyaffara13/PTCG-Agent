
def test_commutation():
    n, m = symbols("n,m", above_fermi=True)
    c = Commutator(B(0), Bd(0))
    assert c == 1
    c = Commutator(Bd(0), B(0))
    assert c == -1
    c = Commutator(B(n), Bd(0))
    assert c == KroneckerDelta(n, 0)
    c = Commutator(B(0), B(0))
    assert c == 0
    c = Commutator(B(0), Bd(0))
    e = simplify(apply_operators(c*BKet([n])))
    assert e == BKet([n])
    c = Commutator(B(0), B(1))
    e = simplify(apply_operators(c*BKet([n, m])))
    assert e == 0

    c = Commutator(F(m), Fd(m))
    assert c == +1 - 2*NO(Fd(m)*F(m))
    c = Commutator(Fd(m), F(m))
    assert c.expand() == -1 + 2*NO(Fd(m)*F(m))

    C = Commutator
    X, Y, Z = symbols('X,Y,Z', commutative=False)
    assert C(C(X, Y), Z) != 0
    assert C(C(X, Z), Y) != 0
    assert C(Y, C(X, Z)) != 0

    i, j, k, l = symbols('i,j,k,l', below_fermi=True)
    a, b, c, d = symbols('a,b,c,d', above_fermi=True)
    p, q, r, s = symbols('p,q,r,s')
    D = KroneckerDelta

    assert C(Fd(a), F(i)) == -2*NO(F(i)*Fd(a))
    assert C(Fd(j), NO(Fd(a)*F(i))).doit(wicks=True) == -D(j, i)*Fd(a)
    assert C(Fd(a)*F(i), Fd(b)*F(j)).doit(wicks=True) == 0

    c1 = Commutator(F(a), Fd(a))
    assert Commutator.eval(c1, c1) == 0
    c = Commutator(Fd(a)*F(i),Fd(b)*F(j))
    assert latex(c) == r'\left[{a^\dagger_{a}} a_{i},{a^\dagger_{b}} a_{j}\right]'
    assert repr(c) == 'Commutator(CreateFermion(a)*AnnihilateFermion(i),CreateFermion(b)*AnnihilateFermion(j))'
    assert str(c) == '[CreateFermion(a)*AnnihilateFermion(i),CreateFermion(b)*AnnihilateFermion(j)]'

