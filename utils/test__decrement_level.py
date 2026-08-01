
def test_DecrementLevel():
    DE = DifferentialExtension(x*log(exp(x) + 1), x)
    assert DE.level == -1
    assert DE.t == t1
    assert DE.d == Poly(t0/(t0 + 1), t1)
    assert DE.case == 'primitive'

    with DecrementLevel(DE):
        assert DE.level == -2
        assert DE.t == t0
        assert DE.d == Poly(t0, t0)
        assert DE.case == 'exp'

        with DecrementLevel(DE):
            assert DE.level == -3
            assert DE.t == x
            assert DE.d == Poly(1, x)
            assert DE.case == 'base'

        assert DE.level == -2
        assert DE.t == t0
        assert DE.d == Poly(t0, t0)
        assert DE.case == 'exp'

    assert DE.level == -1
    assert DE.t == t1
    assert DE.d == Poly(t0/(t0 + 1), t1)
    assert DE.case == 'primitive'

    # Test that __exit__ is called after an exception correctly
    try:
        with DecrementLevel(DE):
            raise _TestingException
    except _TestingException:
        pass
    else:
        raise AssertionError("Did not raise.")

    assert DE.level == -1
    assert DE.t == t1
    assert DE.d == Poly(t0/(t0 + 1), t1)
    assert DE.case == 'primitive'

