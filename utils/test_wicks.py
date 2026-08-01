
def test_wicks():
    p, q, r, s = symbols('p,q,r,s', above_fermi=True)

    # Testing for particles only

    str = F(p)*Fd(q)
    assert wicks(str) == NO(F(p)*Fd(q)) + KroneckerDelta(p, q)
    str = Fd(p)*F(q)
    assert wicks(str) == NO(Fd(p)*F(q))

    str = F(p)*Fd(q)*F(r)*Fd(s)
    nstr = wicks(str)
    fasit = NO(
        KroneckerDelta(p, q)*KroneckerDelta(r, s)
        + KroneckerDelta(p, q)*AnnihilateFermion(r)*CreateFermion(s)
        + KroneckerDelta(r, s)*AnnihilateFermion(p)*CreateFermion(q)
        - KroneckerDelta(p, s)*AnnihilateFermion(r)*CreateFermion(q)
        - AnnihilateFermion(p)*AnnihilateFermion(r)*CreateFermion(q)*CreateFermion(s))
    assert nstr == fasit

    assert (p*q*nstr).expand() == wicks(p*q*str)
    assert (nstr*p*q*2).expand() == wicks(str*p*q*2)

    # Testing CC equations particles and holes
    i, j, k, l = symbols('i j k l', below_fermi=True, cls=Dummy)
    a, b, c, d = symbols('a b c d', above_fermi=True, cls=Dummy)
    p, q, r, s = symbols('p q r s', cls=Dummy)

    assert (wicks(F(a)*NO(F(i)*F(j))*Fd(b)) ==
            NO(F(a)*F(i)*F(j)*Fd(b)) +
            KroneckerDelta(a, b)*NO(F(i)*F(j)))
    assert (wicks(F(a)*NO(F(i)*F(j)*F(k))*Fd(b)) ==
            NO(F(a)*F(i)*F(j)*F(k)*Fd(b)) -
            KroneckerDelta(a, b)*NO(F(i)*F(j)*F(k)))

    expr = wicks(Fd(i)*NO(Fd(j)*F(k))*F(l))
    assert (expr ==
           -KroneckerDelta(i, k)*NO(Fd(j)*F(l)) -
            KroneckerDelta(j, l)*NO(Fd(i)*F(k)) -
            KroneckerDelta(i, k)*KroneckerDelta(j, l) +
            KroneckerDelta(i, l)*NO(Fd(j)*F(k)) +
            NO(Fd(i)*Fd(j)*F(k)*F(l)))
    expr = wicks(F(a)*NO(F(b)*Fd(c))*Fd(d))
    assert (expr ==
           -KroneckerDelta(a, c)*NO(F(b)*Fd(d)) -
            KroneckerDelta(b, d)*NO(F(a)*Fd(c)) -
            KroneckerDelta(a, c)*KroneckerDelta(b, d) +
            KroneckerDelta(a, d)*NO(F(b)*Fd(c)) +
            NO(F(a)*F(b)*Fd(c)*Fd(d)))

