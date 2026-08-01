
def test_asec_leading_term():
    assert asec(1/x).as_leading_term(x) == pi/2
    # Tests concerning branch points
    assert asec(x + 1).as_leading_term(x) == sqrt(2)*sqrt(x)
    assert asec(x - 1).as_leading_term(x) == pi
    # Tests concerning points lying on branch cuts
    assert asec(x).as_leading_term(x, cdir=1) == -I*log(x) + I*log(2)
    assert asec(x).as_leading_term(x, cdir=-1) == I*log(x) + 2*pi - I*log(2)
    assert asec(I*x + 1/2).as_leading_term(x, cdir=1) == asec(1/2)
    assert asec(-I*x + 1/2).as_leading_term(x, cdir=1) == -asec(1/2)
    assert asec(I*x - 1/2).as_leading_term(x, cdir=1) == 2*pi - asec(-1/2)
    assert asec(-I*x - 1/2).as_leading_term(x, cdir=1) == asec(-1/2)
    # Tests concerning im(ndir) == 0
    assert asec(-I*x**2 + x - S(1)/2).as_leading_term(x, cdir=1) == pi + I*log(2 - sqrt(3))
    assert asec(-I*x**2 + x - S(1)/2).as_leading_term(x, cdir=-1) == pi + I*log(2 - sqrt(3))

