
def test_Rational_number():
    r = Rational(3, 4)
    assert ask(Q.commutative(r)) is True
    assert ask(Q.integer(r)) is False
    assert ask(Q.rational(r)) is True
    assert ask(Q.real(r)) is True
    assert ask(Q.complex(r)) is True
    assert ask(Q.irrational(r)) is False
    assert ask(Q.imaginary(r)) is False
    assert ask(Q.positive(r)) is True
    assert ask(Q.negative(r)) is False
    assert ask(Q.even(r)) is False
    assert ask(Q.odd(r)) is False
    assert ask(Q.finite(r)) is True
    assert ask(Q.prime(r)) is False
    assert ask(Q.composite(r)) is False
    assert ask(Q.hermitian(r)) is True
    assert ask(Q.antihermitian(r)) is False

    r = Rational(1, 4)
    assert ask(Q.positive(r)) is True
    assert ask(Q.negative(r)) is False

    r = Rational(5, 4)
    assert ask(Q.negative(r)) is False
    assert ask(Q.positive(r)) is True

    r = Rational(5, 3)
    assert ask(Q.positive(r)) is True
    assert ask(Q.negative(r)) is False

    r = Rational(-3, 4)
    assert ask(Q.positive(r)) is False
    assert ask(Q.negative(r)) is True

    r = Rational(-1, 4)
    assert ask(Q.positive(r)) is False
    assert ask(Q.negative(r)) is True

    r = Rational(-5, 4)
    assert ask(Q.negative(r)) is True
    assert ask(Q.positive(r)) is False

    r = Rational(-5, 3)
    assert ask(Q.positive(r)) is False
    assert ask(Q.negative(r)) is True

