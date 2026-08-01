
def test_issue_11746():
    assert (1/x).subs(x**2, 1) == 1/x
    assert (1/(x**3)).subs(x**2, 1) == x**(-3)
    assert (1/(x**4)).subs(x**2, 1) == 1
    assert (1/(x**3)).subs(x**4, 1) == x**(-3)
    assert (1/(y**5)).subs(x**5, 1) == y**(-5)

