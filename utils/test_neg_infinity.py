
def test_neg_infinity():
    mm = S.NegativeInfinity

    assert mm.is_commutative is True
    assert mm.is_integer is False
    assert mm.is_rational is False
    assert mm.is_algebraic is False
    assert mm.is_transcendental is False
    assert mm.is_extended_real is True
    assert mm.is_real is False
    assert mm.is_complex is False
    assert mm.is_noninteger is True
    assert mm.is_irrational is False
    assert mm.is_imaginary is False
    assert mm.is_nonzero is False
    assert mm.is_positive is False
    assert mm.is_negative is False
    assert mm.is_nonpositive is False
    assert mm.is_nonnegative is False
    assert mm.is_extended_nonzero is True
    assert mm.is_extended_positive is False
    assert mm.is_extended_negative is True
    assert mm.is_extended_nonpositive is True
    assert mm.is_extended_nonnegative is False
    assert mm.is_even is False
    assert mm.is_odd is False
    assert mm.is_finite is False
    assert mm.is_infinite is True
    assert mm.is_comparable is True
    assert mm.is_prime is False
    assert mm.is_composite is False
    assert mm.is_number is True


def test_neg_infinity():
    mm = S.NegativeInfinity
    assert ask(Q.commutative(mm)) is True
    assert ask(Q.integer(mm)) is False
    assert ask(Q.rational(mm)) is False
    assert ask(Q.algebraic(mm)) is False
    assert ask(Q.real(mm)) is False
    assert ask(Q.extended_real(mm)) is True
    assert ask(Q.complex(mm)) is False
    assert ask(Q.irrational(mm)) is False
    assert ask(Q.imaginary(mm)) is False
    assert ask(Q.positive(mm)) is False
    assert ask(Q.negative(mm)) is False
    assert ask(Q.extended_negative(mm)) is True
    assert ask(Q.even(mm)) is False
    assert ask(Q.odd(mm)) is False
    assert ask(Q.finite(mm)) is False
    assert ask(Q.infinite(oo)) is True
    assert ask(Q.prime(mm)) is False
    assert ask(Q.composite(mm)) is False
    assert ask(Q.hermitian(mm)) is False
    assert ask(Q.antihermitian(mm)) is False
    assert ask(Q.positive_infinite(-oo)) is False
    assert ask(Q.negative_infinite(-oo)) is True

