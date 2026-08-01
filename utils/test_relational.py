
def test_relational():
    if not np:
        skip("NumPy not installed")

    e = Equality(x, 1)

    f = lambdify((x,), e)
    x_ = np.array([0, 1, 2])
    assert np.array_equal(f(x_), [False, True, False])

    e = Unequality(x, 1)

    f = lambdify((x,), e)
    x_ = np.array([0, 1, 2])
    assert np.array_equal(f(x_), [True, False, True])

    e = (x < 1)

    f = lambdify((x,), e)
    x_ = np.array([0, 1, 2])
    assert np.array_equal(f(x_), [True, False, False])

    e = (x <= 1)

    f = lambdify((x,), e)
    x_ = np.array([0, 1, 2])
    assert np.array_equal(f(x_), [True, True, False])

    e = (x > 1)

    f = lambdify((x,), e)
    x_ = np.array([0, 1, 2])
    assert np.array_equal(f(x_), [False, False, True])

    e = (x >= 1)

    f = lambdify((x,), e)
    x_ = np.array([0, 1, 2])
    assert np.array_equal(f(x_), [False, True, True])


def test_relational():
    from sympy.core.relational import Lt
    assert (pi < 3) is S.false
    assert (pi <= 3) is S.false
    assert (pi > 3) is S.true
    assert (pi >= 3) is S.true
    assert (-pi < 3) is S.true
    assert (-pi <= 3) is S.true
    assert (-pi > 3) is S.false
    assert (-pi >= 3) is S.false
    r = Symbol('r', real=True)
    assert (r - 2 < r - 3) is S.false
    assert Lt(x + I, x + I + 2).func == Lt  # issue 8288


def test_relational():
    # real
    x = S(.1)
    assert (x != cos) is True
    assert (x == cos) is False

    # rational
    x = Rational(1, 3)
    assert (x != cos) is True
    assert (x == cos) is False

    # integer defers to rational so these tests are omitted

    # number symbol
    x = pi
    assert (x != cos) is True
    assert (x == cos) is False


def test_relational():
    assert ask(Q.eq(x, 0), Q.zero(x))
    assert not ask(Q.eq(x, 0), Q.nonzero(x))
    assert not ask(Q.ne(x, 0), Q.zero(x))
    assert ask(Q.ne(x, 0), Q.nonzero(x))

