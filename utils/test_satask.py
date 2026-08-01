
def test_satask():
    # No relevant facts
    assert satask(Q.real(x), Q.real(x)) is True
    assert satask(Q.real(x), ~Q.real(x)) is False
    assert satask(Q.real(x)) is None

    assert satask(Q.real(x), Q.positive(x)) is True
    assert satask(Q.positive(x), Q.real(x)) is None
    assert satask(Q.real(x), ~Q.positive(x)) is None
    assert satask(Q.positive(x), ~Q.real(x)) is False

    raises(ValueError, lambda: satask(Q.real(x), Q.real(x) & ~Q.real(x)))

    with assuming(Q.positive(x)):
        assert satask(Q.real(x)) is True
        assert satask(~Q.positive(x)) is False
        raises(ValueError, lambda: satask(Q.real(x), ~Q.positive(x)))

    assert satask(Q.zero(x), Q.nonzero(x)) is False
    assert satask(Q.positive(x), Q.zero(x)) is False
    assert satask(Q.real(x), Q.zero(x)) is True
    assert satask(Q.zero(x), Q.zero(x*y)) is None
    assert satask(Q.zero(x*y), Q.zero(x))

