
def test_issue_10161():
    x = symbols('x', real=True)
    assert x*abs(x)*abs(x) == x**3

