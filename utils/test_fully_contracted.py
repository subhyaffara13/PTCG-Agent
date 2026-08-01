
def test_fully_contracted():
    i, j, k, l = symbols('i j k l', below_fermi=True)
    a, b, c, d = symbols('a b c d', above_fermi=True)
    p, q, r, s = symbols('p q r s', cls=Dummy)

    Fock = (AntiSymmetricTensor('f', (p,), (q,))*
            NO(Fd(p)*F(q)))
    V = (AntiSymmetricTensor('v', (p, q), (r, s))*
         NO(Fd(p)*Fd(q)*F(s)*F(r)))/4

    Fai = wicks(NO(Fd(i)*F(a))*Fock,
            keep_only_fully_contracted=True,
            simplify_kronecker_deltas=True)
    assert Fai == AntiSymmetricTensor('f', (a,), (i,))
    Vabij = wicks(NO(Fd(i)*Fd(j)*F(b)*F(a))*V,
            keep_only_fully_contracted=True,
            simplify_kronecker_deltas=True)
    assert Vabij == AntiSymmetricTensor('v', (a, b), (i, j))

