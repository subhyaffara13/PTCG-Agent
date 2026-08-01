
def test_issues_8632_8633_8638_8675_8992():
    p = Dummy(integer=True, positive=True)
    nn = Dummy(integer=True, nonnegative=True)
    assert (p - S.Half).is_positive
    assert (p - 1).is_nonnegative
    assert (nn + 1).is_positive
    assert (-p + 1).is_nonpositive
    assert (-nn - 1).is_negative
    prime = Dummy(prime=True)
    assert (prime - 2).is_nonnegative
    assert (prime - 3).is_nonnegative is None
    even = Dummy(positive=True, even=True)
    assert (even - 2).is_nonnegative

    p = Dummy(positive=True)
    assert (p/(p + 1) - 1).is_negative
    assert ((p + 2)**3 - S.Half).is_positive
    n = Dummy(negative=True)
    assert (n - 3).is_nonpositive

