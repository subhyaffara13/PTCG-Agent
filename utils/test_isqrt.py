
def test_isqrt():
    from math import sqrt as _sqrt
    limit = 4503599761588223
    assert int(_sqrt(limit)) == integer_nthroot(limit, 2)[0]
    assert int(_sqrt(limit + 1)) != integer_nthroot(limit + 1, 2)[0]
    assert isqrt(limit + 1) == integer_nthroot(limit + 1, 2)[0]
    assert isqrt(limit + S.Half) == integer_nthroot(limit, 2)[0]
    assert isqrt(limit + 1 + S.Half) == integer_nthroot(limit + 1, 2)[0]
    assert isqrt(limit + 2 + S.Half) == integer_nthroot(limit + 2, 2)[0]

    # Regression tests for https://github.com/sympy/sympy/issues/17034
    assert isqrt(4503599761588224) == 67108864
    assert isqrt(9999999999999999) == 99999999

    # Other corner cases, especially involving non-integers.
    raises(ValueError, lambda: isqrt(-1))
    raises(ValueError, lambda: isqrt(-10**1000))
    raises(ValueError, lambda: isqrt(Rational(-1, 2)))

    tiny = Rational(1, 10**1000)
    raises(ValueError, lambda: isqrt(-tiny))
    assert isqrt(1-tiny) == 0
    assert isqrt(4503599761588224-tiny) == 67108864
    assert isqrt(10**100 - tiny) == 10**50 - 1

