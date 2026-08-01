
def test_TribonacciConstant():
    assert str(TribonacciConstant) == "TribonacciConstant"


def test_TribonacciConstant():
    z = S.TribonacciConstant
    assert ask(Q.commutative(z)) is True
    assert ask(Q.integer(z)) is False
    assert ask(Q.rational(z)) is False
    assert ask(Q.algebraic(z)) is True
    assert ask(Q.real(z)) is True
    assert ask(Q.complex(z)) is True
    assert ask(Q.irrational(z)) is True
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

