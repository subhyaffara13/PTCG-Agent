
def test_int_NumberSymbols():
    assert int(Catalan) == 0
    assert int(EulerGamma) == 0
    assert int(pi) == 3
    assert int(E) == 2
    assert int(GoldenRatio) == 1
    assert int(TribonacciConstant) == 1
    for i in [Catalan, E, EulerGamma, GoldenRatio, TribonacciConstant, pi]:
        a, b = i.approximation_interval(Integer)
        ia = int(i)
        assert ia == a
        assert isinstance(ia, int)
        assert b == a + 1
        assert a.is_Integer and b.is_Integer

