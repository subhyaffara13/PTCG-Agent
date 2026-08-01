
def test_asin_leading_term():
    assert asin(x).as_leading_term(x) == x
    # Tests concerning branch points
    assert asin(x + 1).as_leading_term(x) == pi/2
    assert asin(x - 1).as_leading_term(x) == -pi/2
    assert asin(1/x).as_leading_term(x, cdir=1) == I*log(x) + pi/2 - I*log(2)
    assert asin(1/x).as_leading_term(x, cdir=-1) == -I*log(x) - 3*pi/2 + I*log(2)
    # Tests concerning points lying on branch cuts
    assert asin(I*x + 2).as_leading_term(x, cdir=1) == pi - asin(2)
    assert asin(-I*x + 2).as_leading_term(x, cdir=1) == asin(2)
    assert asin(I*x - 2).as_leading_term(x, cdir=1) == -asin(2)
    assert asin(-I*x - 2).as_leading_term(x, cdir=1) == -pi + asin(2)
    # Tests concerning im(ndir) == 0
    assert asin(-I*x**2 + x - 2).as_leading_term(x, cdir=1) == -pi/2 + I*log(2 - sqrt(3))
    assert asin(-I*x**2 + x - 2).as_leading_term(x, cdir=-1) == -pi/2 + I*log(2 - sqrt(3))

