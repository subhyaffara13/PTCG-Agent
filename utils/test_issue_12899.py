
def test_issue_12899():
    assert manualintegrate(f(x,y).diff(x),y) == Integral(Derivative(f(x,y),x),y)
    assert manualintegrate(f(x,y).diff(y).diff(x),y) == Derivative(f(x,y),x)

