
def test_zero_pow():
    assert satask(Q.zero(x**y), Q.zero(x) & Q.positive(y)) is True
    assert satask(Q.zero(x**y), Q.nonzero(x) & Q.zero(y)) is False

    assert satask(Q.zero(x), Q.zero(x**y)) is True

    assert satask(Q.zero(x**y), Q.zero(x)) is None

