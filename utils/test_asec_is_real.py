
def test_asec_is_real():
    assert asec(S.Half).is_real is False
    n = Symbol('n', positive=True, integer=True)
    assert asec(n).is_extended_real is True
    assert asec(x).is_real is None
    assert asec(r).is_real is None
    t = Symbol('t', real=False, finite=True)
    assert asec(t).is_real is False

