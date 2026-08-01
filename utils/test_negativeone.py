
def test_negativeone():
    z = Integer(-1)
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
    assert z.is_negative is True
    assert z.is_nonpositive is True
    assert z.is_nonnegative is False
    assert z.is_even is False
    assert z.is_odd is True
    assert z.is_finite is True
    assert z.is_infinite is False
    assert z.is_comparable is True
    assert z.is_prime is False
    assert z.is_composite is False
    assert z.is_number is True


def test_negativeone():
    z = Integer(-1)
    assert ask(Q.nonzero(z)) is True
    assert ask(Q.zero(z)) is False
    assert ask(Q.commutative(z)) is True
    assert ask(Q.integer(z)) is True
    assert ask(Q.rational(z)) is True
    assert ask(Q.real(z)) is True
    assert ask(Q.complex(z)) is True
    assert ask(Q.irrational(z)) is False
    assert ask(Q.imaginary(z)) is False
    assert ask(Q.positive(z)) is False
    assert ask(Q.negative(z)) is True
    assert ask(Q.even(z)) is False
    assert ask(Q.odd(z)) is True
    assert ask(Q.finite(z)) is True
    assert ask(Q.prime(z)) is False
    assert ask(Q.composite(z)) is False
    assert ask(Q.hermitian(z)) is True
    assert ask(Q.antihermitian(z)) is False

