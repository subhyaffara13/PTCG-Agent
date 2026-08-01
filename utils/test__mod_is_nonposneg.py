
def test_Mod_is_nonposneg():
    n = Symbol('n', integer=True)
    k = Symbol('k', integer=True, positive=True)
    assert (n%3).is_nonnegative
    assert Mod(n, -3).is_nonpositive
    assert Mod(n, k).is_nonnegative
    assert Mod(n, -k).is_nonpositive
    assert Mod(k, n).is_nonnegative is None

