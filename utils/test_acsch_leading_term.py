
def test_acsch_leading_term():
    x = Symbol('x')
    assert acsch(1/x).as_leading_term(x) == x
    # Tests concerning branch points
    assert acsch(x + I).as_leading_term(x) == -I*pi/2
    assert acsch(x - I).as_leading_term(x) == I*pi/2
    # Tests concerning points lying on branch cuts
    assert acsch(x).as_leading_term(x, cdir=1) == -log(x) + log(2)
    assert acsch(x).as_leading_term(x, cdir=-1) == log(x) - log(2) - I*pi
    assert acsch(x + I/2).as_leading_term(x, cdir=1) == -I*pi - acsch(I/2)
    assert acsch(x + I/2).as_leading_term(x, cdir=-1) == acsch(I/2)
    assert acsch(x - I/2).as_leading_term(x, cdir=1) == -acsch(I/2)
    assert acsch(x - I/2).as_leading_term(x, cdir=-1) == acsch(I/2) + I*pi
    # Tests concerning re(ndir) == 0
    assert acsch(I/2 + I*x - x**2).as_leading_term(x, cdir=1) == log(2 - sqrt(3)) - I*pi/2
    assert acsch(I/2 + I*x - x**2).as_leading_term(x, cdir=-1) == log(2 - sqrt(3)) - I*pi/2

