
def test_acsc_leading_term():
    assert acsc(1/x).as_leading_term(x) == x
    # Tests concerning branch points
    assert acsc(x + 1).as_leading_term(x) == pi/2
    assert acsc(x - 1).as_leading_term(x) == -pi/2
    # Tests concerning points lying on branch cuts
    assert acsc(x).as_leading_term(x, cdir=1) == I*log(x) + pi/2 - I*log(2)
    assert acsc(x).as_leading_term(x, cdir=-1) == -I*log(x) - 3*pi/2 + I*log(2)
    assert acsc(I*x + 1/2).as_leading_term(x, cdir=1) == acsc(1/2)
    assert acsc(-I*x + 1/2).as_leading_term(x, cdir=1) == pi - acsc(1/2)
    assert acsc(I*x - 1/2).as_leading_term(x, cdir=1) == -pi - acsc(-1/2)
    assert acsc(-I*x - 1/2).as_leading_term(x, cdir=1) == -acsc(1/2)
    # Tests concerning im(ndir) == 0
    assert acsc(-I*x**2 + x - S(1)/2).as_leading_term(x, cdir=1) == -pi/2 + I*log(sqrt(3) + 2)
    assert acsc(-I*x**2 + x - S(1)/2).as_leading_term(x, cdir=-1) == -pi/2 + I*log(sqrt(3) + 2)

