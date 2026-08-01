
def test_Mul_is_negative_positive_2():
    a = Symbol('a', nonnegative=True)
    b = Symbol('b', nonnegative=True)
    c = Symbol('c', nonpositive=True)
    d = Symbol('d', nonpositive=True)

    assert (a*b).is_nonnegative is True
    assert (a*b).is_negative is False
    assert (a*b).is_zero is None
    assert (a*b).is_positive is None

    assert (c*d).is_nonnegative is True
    assert (c*d).is_negative is False
    assert (c*d).is_zero is None
    assert (c*d).is_positive is None

    assert (a*c).is_nonpositive is True
    assert (a*c).is_positive is False
    assert (a*c).is_zero is None
    assert (a*c).is_negative is None

