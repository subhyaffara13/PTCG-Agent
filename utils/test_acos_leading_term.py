
def test_acos_leading_term():
    assert acos(x).as_leading_term(x) == pi/2
    # Tests concerning branch points
    assert acos(x + 1).as_leading_term(x) == sqrt(2)*sqrt(-x)
    assert acos(x - 1).as_leading_term(x) == pi
    assert acos(1/x).as_leading_term(x, cdir=1) == -I*log(x) + I*log(2)
    assert acos(1/x).as_leading_term(x, cdir=-1) == I*log(x) + 2*pi - I*log(2)
    # Tests concerning points lying on branch cuts
    assert acos(I*x + 2).as_leading_term(x, cdir=1) == -acos(2)
    assert acos(-I*x + 2).as_leading_term(x, cdir=1) == acos(2)
    assert acos(I*x - 2).as_leading_term(x, cdir=1) == acos(-2)
    assert acos(-I*x - 2).as_leading_term(x, cdir=1) == 2*pi - acos(-2)
    # Tests concerning im(ndir) == 0
    assert acos(-I*x**2 + x - 2).as_leading_term(x, cdir=1) == pi + I*log(sqrt(3) + 2)
    assert acos(-I*x**2 + x - 2).as_leading_term(x, cdir=-1) == pi + I*log(sqrt(3) + 2)

