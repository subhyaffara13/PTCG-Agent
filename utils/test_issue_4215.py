
def test_issue_4215():
    x = Symbol("x")
    assert integrate(1/(x**2), (x, -1, 1)) is oo

