
def test_atanh_leading_term():
    x = Symbol('x')
    assert atanh(x).as_leading_term(x) == x
    # Tests concerning branch points
    assert atanh(x + 1).as_leading_term(x, cdir=1) == -log(x)/2 + log(2)/2 - I*pi/2
    assert atanh(x + 1).as_leading_term(x, cdir=-1) == -log(x)/2 + log(2)/2 + I*pi/2
    assert atanh(x - 1).as_leading_term(x, cdir=1) == log(x)/2 - log(2)/2
    assert atanh(x - 1).as_leading_term(x, cdir=-1) == log(x)/2 - log(2)/2
    assert atanh(1/x).as_leading_term(x, cdir=1) == -I*pi/2
    assert atanh(1/x).as_leading_term(x, cdir=-1) == I*pi/2
    # Tests concerning points lying on branch cuts
    assert atanh(I*x + 2).as_leading_term(x, cdir=1) == atanh(2) + I*pi
    assert atanh(-I*x + 2).as_leading_term(x, cdir=1) == atanh(2)
    assert atanh(I*x - 2).as_leading_term(x, cdir=1) == -atanh(2)
    assert atanh(-I*x - 2).as_leading_term(x, cdir=1) == -I*pi - atanh(2)
    # Tests concerning im(ndir) == 0
    assert atanh(-I*x**2 + x - 2).as_leading_term(x, cdir=1) == -log(3)/2 - I*pi/2
    assert atanh(-I*x**2 + x - 2).as_leading_term(x, cdir=-1) == -log(3)/2 - I*pi/2

