
def test_monotonic_sign():
    F = _monotonic_sign
    x = symbols('x')
    assert F(x) is None
    assert F(-x) is None
    assert F(Dummy(prime=True)) == 2
    assert F(Dummy(prime=True, odd=True)) == 3
    assert F(Dummy(composite=True)) == 4
    assert F(Dummy(composite=True, odd=True)) == 9
    assert F(Dummy(positive=True, integer=True)) == 1
    assert F(Dummy(positive=True, even=True)) == 2
    assert F(Dummy(positive=True, even=True, prime=False)) == 4
    assert F(Dummy(negative=True, integer=True)) == -1
    assert F(Dummy(negative=True, even=True)) == -2
    assert F(Dummy(zero=True)) == 0
    assert F(Dummy(nonnegative=True)) == 0
    assert F(Dummy(nonpositive=True)) == 0

    assert F(Dummy(positive=True) + 1).is_positive
    assert F(Dummy(positive=True, integer=True) - 1).is_nonnegative
    assert F(Dummy(positive=True) - 1) is None
    assert F(Dummy(negative=True) + 1) is None
    assert F(Dummy(negative=True, integer=True) - 1).is_nonpositive
    assert F(Dummy(negative=True) - 1).is_negative
    assert F(-Dummy(positive=True) + 1) is None
    assert F(-Dummy(positive=True, integer=True) - 1).is_negative
    assert F(-Dummy(positive=True) - 1).is_negative
    assert F(-Dummy(negative=True) + 1).is_positive
    assert F(-Dummy(negative=True, integer=True) - 1).is_nonnegative
    assert F(-Dummy(negative=True) - 1) is None
    x = Dummy(negative=True)
    assert F(x**3).is_nonpositive
    assert F(x**3 + log(2)*x - 1).is_negative
    x = Dummy(positive=True)
    assert F(-x**3).is_nonpositive

    p = Dummy(positive=True)
    assert F(1/p).is_positive
    assert F(p/(p + 1)).is_positive
    p = Dummy(nonnegative=True)
    assert F(p/(p + 1)).is_nonnegative
    p = Dummy(positive=True)
    assert F(-1/p).is_negative
    p = Dummy(nonpositive=True)
    assert F(p/(-p + 1)).is_nonpositive

    p = Dummy(positive=True, integer=True)
    q = Dummy(positive=True, integer=True)
    assert F(-2/p/q).is_negative
    assert F(-2/(p - 1)/q) is None

    assert F((p - 1)*q + 1).is_positive
    assert F(-(p - 1)*q - 1).is_negative

