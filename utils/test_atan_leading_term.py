
def test_atan_leading_term():
    assert atan(x).as_leading_term(x) == x
    assert atan(1/x).as_leading_term(x, cdir=1) == pi/2
    assert atan(1/x).as_leading_term(x, cdir=-1) == -pi/2
    # Tests concerning branch points
    assert atan(x + I).as_leading_term(x, cdir=1) == -I*log(x)/2 + pi/4 + I*log(2)/2
    assert atan(x + I).as_leading_term(x, cdir=-1) == -I*log(x)/2 - 3*pi/4 + I*log(2)/2
    assert atan(x - I).as_leading_term(x, cdir=1) == I*log(x)/2 + pi/4 - I*log(2)/2
    assert atan(x - I).as_leading_term(x, cdir=-1) == I*log(x)/2 + pi/4 - I*log(2)/2
    # Tests concerning points lying on branch cuts
    assert atan(x + 2*I).as_leading_term(x, cdir=1) == I*atanh(2)
    assert atan(x + 2*I).as_leading_term(x, cdir=-1) == -pi + I*atanh(2)
    assert atan(x - 2*I).as_leading_term(x, cdir=1) == pi - I*atanh(2)
    assert atan(x - 2*I).as_leading_term(x, cdir=-1) == -I*atanh(2)
    # Tests concerning re(ndir) == 0
    assert atan(2*I - I*x - x**2).as_leading_term(x, cdir=1) == -pi/2 + I*log(3)/2
    assert atan(2*I - I*x - x**2).as_leading_term(x, cdir=-1) == -pi/2 + I*log(3)/2

