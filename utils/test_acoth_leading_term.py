
def test_acoth_leading_term():
    x = Symbol('x')
    # Tests concerning branch points
    assert acoth(x + 1).as_leading_term(x, cdir=1) == -log(x)/2 + log(2)/2
    assert acoth(x + 1).as_leading_term(x, cdir=-1) == -log(x)/2 + log(2)/2
    assert acoth(x - 1).as_leading_term(x, cdir=1) == log(x)/2 - log(2)/2 + I*pi/2
    assert acoth(x - 1).as_leading_term(x, cdir=-1) == log(x)/2 - log(2)/2 - I*pi/2
    # Tests concerning points lying on branch cuts
    assert acoth(x).as_leading_term(x, cdir=-1) == I*pi/2
    assert acoth(x).as_leading_term(x, cdir=1) == -I*pi/2
    assert acoth(I*x + 1/2).as_leading_term(x, cdir=1) == acoth(1/2)
    assert acoth(-I*x + 1/2).as_leading_term(x, cdir=1) == acoth(1/2) + I*pi
    assert acoth(I*x - 1/2).as_leading_term(x, cdir=1) == -I*pi - acoth(1/2)
    assert acoth(-I*x - 1/2).as_leading_term(x, cdir=1) == -acoth(1/2)
    # Tests concerning im(ndir) == 0
    assert acoth(-I*x**2 - x - S(1)/2).as_leading_term(x, cdir=1) == -log(3)/2 + I*pi/2
    assert acoth(-I*x**2 - x - S(1)/2).as_leading_term(x, cdir=-1) == -log(3)/2 + I*pi/2

