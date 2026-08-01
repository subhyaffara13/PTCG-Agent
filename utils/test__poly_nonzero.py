
def test_Poly_nonzero():
    assert not bool(Poly(0, x)) is True
    assert not bool(Poly(1, x)) is False

