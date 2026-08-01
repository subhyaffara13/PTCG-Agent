
def test_high_order_multivariate():
    assert len(solve(a*x**3 - x + 1, x)) == 3
    assert len(solve(a*x**4 - x + 1, x)) == 4
    assert solve(a*x**5 - x + 1, x) == []  # incomplete solution allowed
    raises(NotImplementedError, lambda:
        solve(a*x**5 - x + 1, x, incomplete=False))

    # result checking must always consider the denominator and CRootOf
    # must be checked, too
    d = x**5 - x + 1
    assert solve(d*(1 + 1/d)) == [CRootOf(d + 1, i) for i in range(5)]
    d = x - 1
    assert solve(d*(2 + 1/d)) == [S.Half]

