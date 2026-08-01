
def test_S_srepr_is_identity():
    p = Piecewise((10, Eq(x, 0)), (12, True))
    q = S(srepr(p))
    assert p == q

