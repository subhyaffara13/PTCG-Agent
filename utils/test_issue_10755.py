
def test_issue_10755():
    x = symbols('x')
    raises(TypeError, lambda: int(log(x)))
    raises(TypeError, lambda: log(x).round(2))

