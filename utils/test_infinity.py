
def test_infinity():
    assert sstr(oo*I) == "oo*I"


def test_infinity():
    oo = S.Infinity

    assert oo.is_commutative is True
    assert oo.is_integer is False
    assert oo.is_rational is False
    assert oo.is_algebraic is False
    assert oo.is_transcendental is False
    assert oo.is_extended_real is True
    assert oo.is_real is False
    assert oo.is_complex is False
    assert oo.is_noninteger is True
    assert oo.is_irrational is False
    assert oo.is_imaginary is False
    assert oo.is_nonzero is False
    assert oo.is_positive is False
    assert oo.is_negative is False
    assert oo.is_nonpositive is False
    assert oo.is_nonnegative is False
    assert oo.is_extended_nonzero is True
    assert oo.is_extended_positive is True
    assert oo.is_extended_negative is False
    assert oo.is_extended_nonpositive is False
    assert oo.is_extended_nonnegative is True
    assert oo.is_even is False
    assert oo.is_odd is False
    assert oo.is_finite is False
    assert oo.is_infinite is True
    assert oo.is_comparable is True
    assert oo.is_prime is False
    assert oo.is_composite is False
    assert oo.is_number is True


def test_infinity():
    assert ask(Q.commutative(oo)) is True
    assert ask(Q.integer(oo)) is False
    assert ask(Q.rational(oo)) is False
    assert ask(Q.algebraic(oo)) is False
    assert ask(Q.real(oo)) is False
    assert ask(Q.extended_real(oo)) is True
    assert ask(Q.complex(oo)) is False
    assert ask(Q.irrational(oo)) is False
    assert ask(Q.imaginary(oo)) is False
    assert ask(Q.positive(oo)) is False
    assert ask(Q.extended_positive(oo)) is True
    assert ask(Q.negative(oo)) is False
    assert ask(Q.even(oo)) is False
    assert ask(Q.odd(oo)) is False
    assert ask(Q.finite(oo)) is False
    assert ask(Q.infinite(oo)) is True
    assert ask(Q.prime(oo)) is False
    assert ask(Q.composite(oo)) is False
    assert ask(Q.hermitian(oo)) is False
    assert ask(Q.antihermitian(oo)) is False
    assert ask(Q.positive_infinite(oo)) is True
    assert ask(Q.negative_infinite(oo)) is False

