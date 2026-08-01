
def test_complex_infinity():
    assert ask(Q.commutative(zoo)) is True
    assert ask(Q.integer(zoo)) is False
    assert ask(Q.rational(zoo)) is False
    assert ask(Q.algebraic(zoo)) is False
    assert ask(Q.real(zoo)) is False
    assert ask(Q.extended_real(zoo)) is False
    assert ask(Q.complex(zoo)) is False
    assert ask(Q.irrational(zoo)) is False
    assert ask(Q.imaginary(zoo)) is False
    assert ask(Q.positive(zoo)) is False
    assert ask(Q.negative(zoo)) is False
    assert ask(Q.zero(zoo)) is False
    assert ask(Q.nonzero(zoo)) is False
    assert ask(Q.even(zoo)) is False
    assert ask(Q.odd(zoo)) is False
    assert ask(Q.finite(zoo)) is False
    assert ask(Q.infinite(zoo)) is True
    assert ask(Q.prime(zoo)) is False
    assert ask(Q.composite(zoo)) is False
    assert ask(Q.hermitian(zoo)) is False
    assert ask(Q.antihermitian(zoo)) is False
    assert ask(Q.positive_infinite(zoo)) is False
    assert ask(Q.negative_infinite(zoo)) is False

