
def test_asinh_leading_term():
    x = Symbol('x')
    assert asinh(x).as_leading_term(x, cdir=1) == x
    # Tests concerning branch points
    assert asinh(x + I).as_leading_term(x, cdir=1) == I*pi/2
    assert asinh(x - I).as_leading_term(x, cdir=1) == -I*pi/2
    assert asinh(1/x).as_leading_term(x, cdir=1) == -log(x) + log(2)
    assert asinh(1/x).as_leading_term(x, cdir=-1) == log(x) - log(2) - I*pi
    # Tests concerning points lying on branch cuts
    assert asinh(x + 2*I).as_leading_term(x, cdir=1) == I*asin(2)
    assert asinh(x + 2*I).as_leading_term(x, cdir=-1) == -I*asin(2) + I*pi
    assert asinh(x - 2*I).as_leading_term(x, cdir=1) == -I*pi + I*asin(2)
    assert asinh(x - 2*I).as_leading_term(x, cdir=-1) == -I*asin(2)
    # Tests concerning re(ndir) == 0
    assert asinh(2*I + I*x - x**2).as_leading_term(x, cdir=1) == log(2 - sqrt(3)) + I*pi/2
    assert asinh(2*I + I*x - x**2).as_leading_term(x, cdir=-1) == log(2 - sqrt(3)) + I*pi/2

