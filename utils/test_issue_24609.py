
def test_issue_24609():
    # https://github.com/sympy/sympy/issues/24609
    eq, expected, x = _make_example_24609()
    assert solve(eq, x, simplify=True) == [expected]
    [solapprox] = solve(eq.n(), x)
    assert abs(solapprox - expected.n()) < 1e-14

