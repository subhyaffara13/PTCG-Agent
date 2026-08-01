
def test_acot_leading_term():
    assert acot(1/x).as_leading_term(x) == x
    # Tests concerning branch points
    assert acot(x + I).as_leading_term(x, cdir=1) == I*log(x)/2 + pi/4 - I*log(2)/2
    assert acot(x + I).as_leading_term(x, cdir=-1) == I*log(x)/2 + pi/4 - I*log(2)/2
    assert acot(x - I).as_leading_term(x, cdir=1) == -I*log(x)/2 + pi/4 + I*log(2)/2
    assert acot(x - I).as_leading_term(x, cdir=-1) == -I*log(x)/2 - 3*pi/4 + I*log(2)/2
    # Tests concerning points lying on branch cuts
    assert acot(x).as_leading_term(x, cdir=1) == pi/2
    assert acot(x).as_leading_term(x, cdir=-1) == -pi/2
    assert acot(x + I/2).as_leading_term(x, cdir=1) == pi - I*acoth(S(1)/2)
    assert acot(x + I/2).as_leading_term(x, cdir=-1) == -I*acoth(S(1)/2)
    assert acot(x - I/2).as_leading_term(x, cdir=1) == I*acoth(S(1)/2)
    assert acot(x - I/2).as_leading_term(x, cdir=-1) == -pi + I*acoth(S(1)/2)
    # Tests concerning re(ndir) == 0
    assert acot(I/2 - I*x - x**2).as_leading_term(x, cdir=1) == -pi/2 - I*log(3)/2
    assert acot(I/2 - I*x - x**2).as_leading_term(x, cdir=-1) == -pi/2 - I*log(3)/2

