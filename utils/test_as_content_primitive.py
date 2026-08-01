
def test_as_content_primitive():
    assert (x/2 + y).as_content_primitive() == (S.Half, x + 2*y)
    assert (x/2 + y).as_content_primitive(clear=False) == (S.One, x/2 + y)
    assert (y*(x/2 + y)).as_content_primitive() == (S.Half, y*(x + 2*y))
    assert (y*(x/2 + y)).as_content_primitive(clear=False) == (S.One, y*(x/2 + y))

    # although the _as_content_primitive methods do not alter the underlying structure,
    # the as_content_primitive function will touch up the expression and join
    # bases that would otherwise have not been joined.
    assert (x*(2 + 2*x)*(3*x + 3)**2).as_content_primitive() == \
        (18, x*(x + 1)**3)
    assert (2 + 2*x + 2*y*(3 + 3*y)).as_content_primitive() == \
        (2, x + 3*y*(y + 1) + 1)
    assert ((2 + 6*x)**2).as_content_primitive() == \
        (4, (3*x + 1)**2)
    assert ((2 + 6*x)**(2*y)).as_content_primitive() == \
        (1, (_keep_coeff(S(2), (3*x + 1)))**(2*y))
    assert (5 + 10*x + 2*y*(3 + 3*y)).as_content_primitive() == \
        (1, 10*x + 6*y*(y + 1) + 5)
    assert (5*(x*(1 + y)) + 2*x*(3 + 3*y)).as_content_primitive() == \
        (11, x*(y + 1))
    assert ((5*(x*(1 + y)) + 2*x*(3 + 3*y))**2).as_content_primitive() == \
        (121, x**2*(y + 1)**2)
    assert (y**2).as_content_primitive() == \
        (1, y**2)
    assert (S.Infinity).as_content_primitive() == (1, oo)
    eq = x**(2 + y)
    assert (eq).as_content_primitive() == (1, eq)
    assert (S.Half**(2 + x)).as_content_primitive() == (Rational(1, 4), 2**-x)
    assert (Rational(-1, 2)**(2 + x)).as_content_primitive() == \
           (Rational(1, 4), (Rational(-1, 2))**x)
    assert (Rational(-1, 2)**(2 + x)).as_content_primitive() == \
           (Rational(1, 4), Rational(-1, 2)**x)
    assert (4**((1 + y)/2)).as_content_primitive() == (2, 4**(y/2))
    assert (3**((1 + y)/2)).as_content_primitive() == \
           (1, 3**(Mul(S.Half, 1 + y, evaluate=False)))
    assert (5**Rational(3, 4)).as_content_primitive() == (1, 5**Rational(3, 4))
    assert (5**Rational(7, 4)).as_content_primitive() == (5, 5**Rational(3, 4))
    assert Add(z*Rational(5, 7), 0.5*x, y*Rational(3, 2), evaluate=False).as_content_primitive() == \
              (Rational(1, 14), 7.0*x + 21*y + 10*z)
    assert (2**Rational(3, 4) + 2**Rational(1, 4)*sqrt(3)).as_content_primitive(radical=True) == \
           (1, 2**Rational(1, 4)*(sqrt(2) + sqrt(3)))


def test_as_content_primitive():
    assert S.Zero.as_content_primitive() == (1, 0)
    assert S.Half.as_content_primitive() == (S.Half, 1)
    assert (Rational(-1, 2)).as_content_primitive() == (S.Half, -1)
    assert S(3).as_content_primitive() == (3, 1)
    assert S(3.1).as_content_primitive() == (1, 3.1)

