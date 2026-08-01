
def test_bra():
    b = Bra('0')

    assert isinstance(b, Bra)
    assert isinstance(b, BraBase)
    assert isinstance(b, StateBase)
    assert isinstance(b, QExpr)

    assert b.label == (Symbol('0'),)
    assert b.hilbert_space == HilbertSpace()
    assert b.is_commutative is False

    # Make sure this doesn't get converted to the number pi.
    b = Bra('pi')
    assert b.label == (Symbol('pi'),)

    b = Bra(x, y)
    assert b.label == (x, y)
    assert b.hilbert_space == HilbertSpace()
    assert b.is_commutative is False

    assert b.dual_class() == Ket
    assert b.dual == Ket(x, y)
    assert b.subs(x, y) == Bra(y, y)

    assert Bra() == Bra('psi')

