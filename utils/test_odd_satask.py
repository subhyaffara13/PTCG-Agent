
def test_odd_satask():
    assert satask(Q.odd(2)) is False
    assert satask(Q.odd(3)) is True

    assert satask(Q.odd(x*y), Q.even(x) & Q.odd(y)) is False
    assert satask(Q.odd(x*y), Q.even(x) & Q.integer(y)) is False
    assert satask(Q.odd(x*y), Q.even(x) & Q.even(y)) is False
    assert satask(Q.odd(x*y), Q.odd(x) & Q.odd(y)) is True
    assert satask(Q.odd(x*y), Q.even(x)) is None
    assert satask(Q.odd(x*y), Q.odd(x) & Q.integer(y)) is None
    assert satask(Q.odd(x*y), Q.odd(x) & Q.odd(y)) is True

    assert satask(Q.odd(abs(x)), Q.even(x)) is False
    assert satask(Q.odd(abs(x)), Q.odd(x)) is True
    assert satask(Q.odd(x), Q.odd(abs(x))) is None # x could be complex

