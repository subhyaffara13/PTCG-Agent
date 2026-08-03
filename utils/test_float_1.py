import math


def test_float_1():
    z = 1.0
    assert ask(Q.commutative(z)) is True
    assert ask(Q.integer(z)) is None
    assert ask(Q.rational(z)) is None
    assert ask(Q.real(z)) is True
    assert ask(Q.complex(z)) is True
    assert ask(Q.irrational(z)) is None
    assert ask(Q.imaginary(z)) is False
    assert ask(Q.positive(z)) is True
    assert ask(Q.negative(z)) is False
    assert ask(Q.even(z)) is None
    assert ask(Q.odd(z)) is None
    assert ask(Q.finite(z)) is True
    assert ask(Q.prime(z)) is None
    assert ask(Q.composite(z)) is None
    assert ask(Q.hermitian(z)) is True
    assert ask(Q.antihermitian(z)) is False

    z = 7.2123
    assert ask(Q.commutative(z)) is True
    assert ask(Q.integer(z)) is False
    assert ask(Q.rational(z)) is None
    assert ask(Q.real(z)) is True
    assert ask(Q.complex(z)) is True
    assert ask(Q.irrational(z)) is None
    assert ask(Q.imaginary(z)) is False
    assert ask(Q.positive(z)) is True
    assert ask(Q.negative(z)) is False
    assert ask(Q.even(z)) is False
    assert ask(Q.odd(z)) is False
    assert ask(Q.finite(z)) is True
    assert ask(Q.prime(z)) is False
    assert ask(Q.composite(z)) is False
    assert ask(Q.hermitian(z)) is True
    assert ask(Q.antihermitian(z)) is False

    # test for issue #12168
    assert ask(Q.rational(math.pi)) is None

