
def test_issue_14622():
    assert (x**(-4) + x**(-3) + x**(-1) + O(x**(-6), (x, oo))).as_numer_denom() == (
        x**4 + x**5 + x**7 + O(x**2, (x, oo)), x**8)
    assert (x**3 + O(x**2, (x, oo))).is_Add
    assert O(x**2, (x, oo)).contains(x**3) is False
    assert O(x, (x, oo)).contains(O(x, (x, 0))) is None
    assert O(x, (x, 0)).contains(O(x, (x, oo))) is None
    raises(NotImplementedError, lambda: O(x**3).contains(x**w))

