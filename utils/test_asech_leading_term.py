
def test_asech_leading_term():
    x = Symbol('x')
    # Tests concerning branch points
    assert asech(x).as_leading_term(x, cdir=1) == -log(x) + log(2)
    assert asech(x).as_leading_term(x, cdir=-1) == -log(x) + log(2) + 2*I*pi
    assert asech(x + 1).as_leading_term(x, cdir=1) == sqrt(2)*I*sqrt(x)
    assert asech(1/x).as_leading_term(x, cdir=1) == I*pi/2
    # Tests concerning points lying on branch cuts
    assert asech(x - 1).as_leading_term(x, cdir=1) == I*pi
    assert asech(I*x + 3).as_leading_term(x, cdir=1) == -asech(3)
    assert asech(-I*x + 3).as_leading_term(x, cdir=1) == asech(3)
    assert asech(I*x - 3).as_leading_term(x, cdir=1) == -asech(-3)
    assert asech(-I*x - 3).as_leading_term(x, cdir=1) == asech(-3)
    assert asech(I*x - S(1)/3).as_leading_term(x, cdir=1) == -2*I*pi + asech(-S(1)/3)
    assert asech(I*x - S(1)/3).as_leading_term(x, cdir=-1) == asech(-S(1)/3)
    # Tests concerning im(ndir) == 0
    assert asech(-I*x**2 + x - 3).as_leading_term(x, cdir=1) == log(-S(1)/3 + 2*sqrt(2)*I/3)
    assert asech(-I*x**2 + x - 3).as_leading_term(x, cdir=-1) == log(-S(1)/3 + 2*sqrt(2)*I/3)

