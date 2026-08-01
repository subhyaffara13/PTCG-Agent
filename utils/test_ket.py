
def test_ket():
    k = Ket('0')

    assert isinstance(k, Ket)
    assert isinstance(k, KetBase)
    assert isinstance(k, StateBase)
    assert isinstance(k, QExpr)

    assert k.label == (Symbol('0'),)
    assert k.hilbert_space == HilbertSpace()
    assert k.is_commutative is False

    # Make sure this doesn't get converted to the number pi.
    k = Ket('pi')
    assert k.label == (Symbol('pi'),)

    k = Ket(x, y)
    assert k.label == (x, y)
    assert k.hilbert_space == HilbertSpace()
    assert k.is_commutative is False

    assert k.dual_class() == Bra
    assert k.dual == Bra(x, y)
    assert k.subs(x, y) == Ket(y, y)

    k = CustomKet()
    assert k == CustomKet("test")

    k = CustomKetMultipleLabels()
    assert k == CustomKetMultipleLabels("r", "theta", "phi")

    assert Ket() == Ket('psi')

