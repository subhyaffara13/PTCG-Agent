
def test_issue_7259():
    assert series(LambertW(x), x) == x - x**2 + 3*x**3/2 - 8*x**4/3 + 125*x**5/24 + O(x**6)
    assert series(LambertW(x**2), x, n=8) == x**2 - x**4 + 3*x**6/2 + O(x**8)
    assert series(LambertW(sin(x)), x, n=4) == x - x**2 + 4*x**3/3 + O(x**4)

