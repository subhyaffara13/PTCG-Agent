
def test_rational_irrational():
    assert satask(Q.irrational(2)) is False
    assert satask(Q.rational(2)) is True
    assert satask(Q.irrational(pi)) is True
    assert satask(Q.rational(pi)) is False
    assert satask(Q.irrational(I)) is False
    assert satask(Q.rational(I)) is False

    assert satask(Q.irrational(x*y*z), Q.irrational(x) & Q.irrational(y) &
        Q.rational(z)) is None
    assert satask(Q.irrational(x*y*z), Q.irrational(x) & Q.rational(y) &
        Q.rational(z)) is True
    assert satask(Q.irrational(pi*x*y), Q.rational(x) & Q.rational(y)) is True

    assert satask(Q.irrational(x + y + z), Q.irrational(x) & Q.irrational(y) &
        Q.rational(z)) is None
    assert satask(Q.irrational(x + y + z), Q.irrational(x) & Q.rational(y) &
        Q.rational(z)) is True
    assert satask(Q.irrational(pi + x + y), Q.rational(x) & Q.rational(y)) is True

    assert satask(Q.irrational(x*y*z), Q.rational(x) & Q.rational(y) &
        Q.rational(z)) is False
    assert satask(Q.rational(x*y*z), Q.rational(x) & Q.rational(y) &
        Q.rational(z)) is True

    assert satask(Q.irrational(x + y + z), Q.rational(x) & Q.rational(y) &
        Q.rational(z)) is False
    assert satask(Q.rational(x + y + z), Q.rational(x) & Q.rational(y) &
        Q.rational(z)) is True

