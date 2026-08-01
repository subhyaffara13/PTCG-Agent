
def test_change_mul():
    assert change_mul(x, x) == (None, None)
    assert change_mul(x*y, x) == (None, None)
    assert change_mul(x*y*DiracDelta(x), x) == (DiracDelta(x), x*y)
    assert change_mul(x*y*DiracDelta(x)*DiracDelta(y), x) == \
        (DiracDelta(x), x*y*DiracDelta(y))
    assert change_mul(DiracDelta(x)**2, x) == \
        (DiracDelta(x), DiracDelta(x))
    assert change_mul(y*DiracDelta(x)**2, x) == \
        (DiracDelta(x), y*DiracDelta(x))

