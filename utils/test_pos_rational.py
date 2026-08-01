
def test_pos_rational():
    r = Rational(3, 4)
    assert r.is_commutative is True
    assert r.is_integer is False
    assert r.is_rational is True
    assert r.is_algebraic is True
    assert r.is_transcendental is False
    assert r.is_real is True
    assert r.is_complex is True
    assert r.is_noninteger is True
    assert r.is_irrational is False
    assert r.is_imaginary is False
    assert r.is_positive is True
    assert r.is_negative is False
    assert r.is_nonpositive is False
    assert r.is_nonnegative is True
    assert r.is_even is False
    assert r.is_odd is False
    assert r.is_finite is True
    assert r.is_infinite is False
    assert r.is_comparable is True
    assert r.is_prime is False
    assert r.is_composite is False

    r = Rational(1, 4)
    assert r.is_nonpositive is False
    assert r.is_positive is True
    assert r.is_negative is False
    assert r.is_nonnegative is True
    r = Rational(5, 4)
    assert r.is_negative is False
    assert r.is_positive is True
    assert r.is_nonpositive is False
    assert r.is_nonnegative is True
    r = Rational(5, 3)
    assert r.is_nonnegative is True
    assert r.is_positive is True
    assert r.is_negative is False
    assert r.is_nonpositive is False

