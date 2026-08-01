
def test_bra_ket_dagger():
    x = symbols('x', complex=True)
    k = Ket('k')
    b = Bra('b')
    assert Dagger(k) == Bra('k')
    assert Dagger(b) == Ket('b')
    assert Dagger(k).is_commutative is False

    k2 = Ket('k2')
    e = 2*I*k + x*k2
    assert Dagger(e) == conjugate(x)*Dagger(k2) - 2*I*Dagger(k)

