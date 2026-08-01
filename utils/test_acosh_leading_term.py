
def test_acosh_leading_term():
    x = Symbol('x')
    # Tests concerning branch points
    assert acosh(x).as_leading_term(x) == I*pi/2
    assert acosh(x + 1).as_leading_term(x) == sqrt(2)*sqrt(x)
    assert acosh(x - 1).as_leading_term(x) == I*pi
    assert acosh(1/x).as_leading_term(x, cdir=1) == -log(x) + log(2)
    assert acosh(1/x).as_leading_term(x, cdir=-1) == -log(x) + log(2) + 2*I*pi
    # Tests concerning points lying on branch cuts
    assert acosh(I*x - 2).as_leading_term(x, cdir=1) == acosh(-2)
    assert acosh(-I*x - 2).as_leading_term(x, cdir=1) == -2*I*pi + acosh(-2)
    assert acosh(x**2 - I*x + S(1)/3).as_leading_term(x, cdir=1) == -acosh(S(1)/3)
    assert acosh(x**2 - I*x + S(1)/3).as_leading_term(x, cdir=-1) == acosh(S(1)/3)
    assert acosh(1/(I*x - 3)).as_leading_term(x, cdir=1) == -acosh(-S(1)/3)
    assert acosh(1/(I*x - 3)).as_leading_term(x, cdir=-1) == acosh(-S(1)/3)
    # Tests concerning im(ndir) == 0
    assert acosh(-I*x**2 + x - 2).as_leading_term(x, cdir=1) == log(sqrt(3) + 2) - I*pi
    assert acosh(-I*x**2 + x - 2).as_leading_term(x, cdir=-1) == log(sqrt(3) + 2) - I*pi

