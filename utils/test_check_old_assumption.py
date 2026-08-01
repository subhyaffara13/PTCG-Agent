
def test_check_old_assumption():
    x = symbols('x', real=True)
    assert ask(Q.real(x)) is True
    assert ask(Q.imaginary(x)) is False
    assert ask(Q.complex(x)) is True

    x = symbols('x', imaginary=True)
    assert ask(Q.real(x)) is False
    assert ask(Q.imaginary(x)) is True
    assert ask(Q.complex(x)) is True

    x = symbols('x', complex=True)
    assert ask(Q.real(x)) is None
    assert ask(Q.complex(x)) is True

    x = symbols('x', positive=True)
    assert ask(Q.positive(x)) is True
    assert ask(Q.negative(x)) is False
    assert ask(Q.real(x)) is True

    x = symbols('x', commutative=False)
    assert ask(Q.commutative(x)) is False

    x = symbols('x', negative=True)
    assert ask(Q.positive(x)) is False
    assert ask(Q.negative(x)) is True

    x = symbols('x', nonnegative=True)
    assert ask(Q.negative(x)) is False
    assert ask(Q.positive(x)) is None
    assert ask(Q.zero(x)) is None

    x = symbols('x', finite=True)
    assert ask(Q.finite(x)) is True

    x = symbols('x', prime=True)
    assert ask(Q.prime(x)) is True
    assert ask(Q.composite(x)) is False

    x = symbols('x', composite=True)
    assert ask(Q.prime(x)) is False
    assert ask(Q.composite(x)) is True

    x = symbols('x', even=True)
    assert ask(Q.even(x)) is True
    assert ask(Q.odd(x)) is False

    x = symbols('x', odd=True)
    assert ask(Q.even(x)) is False
    assert ask(Q.odd(x)) is True

    x = symbols('x', nonzero=True)
    assert ask(Q.nonzero(x)) is True
    assert ask(Q.zero(x)) is False

    x = symbols('x', zero=True)
    assert ask(Q.zero(x)) is True

    x = symbols('x', integer=True)
    assert ask(Q.integer(x)) is True

    x = symbols('x', rational=True)
    assert ask(Q.rational(x)) is True
    assert ask(Q.irrational(x)) is False

    x = symbols('x', irrational=True)
    assert ask(Q.irrational(x)) is True
    assert ask(Q.rational(x)) is False

