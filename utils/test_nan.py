
def test_nan():
    assert O(nan) is nan
    assert not O(x).contains(nan)


def test_nan():
    nan = S.NaN

    assert nan.is_commutative is True
    assert nan.is_integer is None
    assert nan.is_rational is None
    assert nan.is_algebraic is None
    assert nan.is_transcendental is None
    assert nan.is_real is None
    assert nan.is_complex is None
    assert nan.is_noninteger is None
    assert nan.is_irrational is None
    assert nan.is_imaginary is None
    assert nan.is_positive is None
    assert nan.is_negative is None
    assert nan.is_nonpositive is None
    assert nan.is_nonnegative is None
    assert nan.is_even is None
    assert nan.is_odd is None
    assert nan.is_finite is None
    assert nan.is_infinite is None
    assert nan.is_comparable is False
    assert nan.is_prime is None
    assert nan.is_composite is None
    assert nan.is_number is True


def test_nan():
    nan = S.NaN
    assert ask(Q.commutative(nan)) is True
    assert ask(Q.integer(nan)) is None
    assert ask(Q.rational(nan)) is None
    assert ask(Q.algebraic(nan)) is None
    assert ask(Q.real(nan)) is None
    assert ask(Q.extended_real(nan)) is None
    assert ask(Q.complex(nan)) is None
    assert ask(Q.irrational(nan)) is None
    assert ask(Q.imaginary(nan)) is None
    assert ask(Q.positive(nan)) is None
    assert ask(Q.nonzero(nan)) is None
    assert ask(Q.zero(nan)) is None
    assert ask(Q.even(nan)) is None
    assert ask(Q.odd(nan)) is None
    assert ask(Q.finite(nan)) is None
    assert ask(Q.infinite(nan)) is None
    assert ask(Q.prime(nan)) is None
    assert ask(Q.composite(nan)) is None
    assert ask(Q.hermitian(nan)) is None
    assert ask(Q.antihermitian(nan)) is None

