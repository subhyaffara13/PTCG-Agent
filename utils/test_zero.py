
def test_zero():
    assert qapply(0) == 0
    assert qapply(Integer(0)) == 0


def test_zero():
    z = Integer(0)
    assert z.is_commutative is True
    assert z.is_integer is True
    assert z.is_rational is True
    assert z.is_algebraic is True
    assert z.is_transcendental is False
    assert z.is_real is True
    assert z.is_complex is True
    assert z.is_noninteger is False
    assert z.is_irrational is False
    assert z.is_imaginary is False
    assert z.is_positive is False
    assert z.is_negative is False
    assert z.is_nonpositive is True
    assert z.is_nonnegative is True
    assert z.is_even is True
    assert z.is_odd is False
    assert z.is_finite is True
    assert z.is_infinite is False
    assert z.is_comparable is True
    assert z.is_prime is False
    assert z.is_composite is False
    assert z.is_number is True


def test_zero():
    assert 0**x != 0
    assert 0**(2*x) == 0**x
    assert 0**(1.0*x) == 0**x
    assert 0**(2.0*x) == 0**x
    assert (0**(2 - x)).as_base_exp() == (0, 2 - x)
    assert 0**(x - 2) != S.Infinity**(2 - x)
    assert 0**(2*x*y) == 0**(x*y)
    assert 0**(-2*x*y) == S.ComplexInfinity**(x*y)
    assert Float(0)**2 is not S.Zero
    assert Float(0)**2 == 0.0
    assert Float(0)**-2 is zoo
    assert Float(0)**oo is S.Zero

    #Test issue 19572
    assert 0 ** -oo is zoo
    assert power(0, -oo) is zoo
    assert Float(0)**-oo is zoo


def test_zero():
    assert ask(Q.zero(x)) is None
    assert ask(Q.zero(x), Q.real(x)) is None
    assert ask(Q.zero(x), Q.positive(x)) is False
    assert ask(Q.zero(x), Q.negative(x)) is False
    assert ask(Q.zero(x), Q.negative(x) | Q.positive(x)) is False

    assert ask(Q.zero(x), Q.nonnegative(x) & Q.nonpositive(x)) is True

    assert ask(Q.zero(x + y)) is None
    assert ask(Q.zero(x + y), Q.positive(x) & Q.positive(y)) is False
    assert ask(Q.zero(x + y), Q.positive(x) & Q.negative(y)) is None
    assert ask(Q.zero(x + y), Q.negative(x) & Q.negative(y)) is False

    assert ask(Q.zero(2*x)) is None
    assert ask(Q.zero(2*x), Q.positive(x)) is False
    assert ask(Q.zero(2*x), Q.negative(x)) is False
    assert ask(Q.zero(x*y), Q.nonzero(x)) is None

    assert ask(Q.zero(Abs(x))) is None
    assert ask(Q.zero(Abs(x)), Q.zero(x)) is True

    assert ask(Q.integer(x), Q.zero(x)) is True
    assert ask(Q.even(x), Q.zero(x)) is True
    assert ask(Q.odd(x), Q.zero(x)) is False
    assert ask(Q.zero(x), Q.even(x)) is None
    assert ask(Q.zero(x), Q.odd(x)) is False
    assert ask(Q.zero(x) | Q.zero(y), Q.zero(x*y)) is True


def test_zero():
    """
    Everything in this test doesn't work with the ask handlers, and most
    things would be very difficult or impossible to make work under that
    model.

    """
    assert satask(Q.zero(x) | Q.zero(y), Q.zero(x*y)) is True
    assert satask(Q.zero(x*y), Q.zero(x) | Q.zero(y)) is True

    assert satask(Implies(Q.zero(x), Q.zero(x*y))) is True

    # This one in particular requires computing the fixed-point of the
    # relevant facts, because going from Q.nonzero(x*y) -> ~Q.zero(x*y) and
    # Q.zero(x*y) -> Equivalent(Q.zero(x*y), Q.zero(x) | Q.zero(y)) takes two
    # steps.
    assert satask(Q.zero(x) | Q.zero(y), Q.nonzero(x*y)) is False

    assert satask(Q.zero(x), Q.zero(x**2)) is True

