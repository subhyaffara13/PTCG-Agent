
def test_zero_positive():
    assert satask(Q.zero(x + y), Q.positive(x) & Q.positive(y)) is False
    assert satask(Q.positive(x) & Q.positive(y), Q.zero(x + y)) is False
    assert satask(Q.nonzero(x + y), Q.positive(x) & Q.positive(y)) is True
    assert satask(Q.positive(x) & Q.positive(y), Q.nonzero(x + y)) is None

    # This one requires several levels of forward chaining
    assert satask(Q.zero(x*(x + y)), Q.positive(x) & Q.positive(y)) is False

    assert satask(Q.positive(pi*x*y + 1), Q.positive(x) & Q.positive(y)) is True
    assert satask(Q.positive(pi*x*y - 5), Q.positive(x) & Q.positive(y)) is None

