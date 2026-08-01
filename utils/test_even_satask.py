
def test_even_satask():
    assert satask(Q.even(2)) is True
    assert satask(Q.even(3)) is False

    assert satask(Q.even(x*y), Q.even(x) & Q.odd(y)) is True
    assert satask(Q.even(x*y), Q.even(x) & Q.integer(y)) is True
    assert satask(Q.even(x*y), Q.even(x) & Q.even(y)) is True
    assert satask(Q.even(x*y), Q.odd(x) & Q.odd(y)) is False
    assert satask(Q.even(x*y), Q.even(x)) is None
    assert satask(Q.even(x*y), Q.odd(x) & Q.integer(y)) is None
    assert satask(Q.even(x*y), Q.odd(x) & Q.odd(y)) is False

    assert satask(Q.even(abs(x)), Q.even(x)) is True
    assert satask(Q.even(abs(x)), Q.odd(x)) is False
    assert satask(Q.even(x), Q.even(abs(x))) is None # x could be complex

