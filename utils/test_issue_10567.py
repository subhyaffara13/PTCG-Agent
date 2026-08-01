
def test_issue_10567():
    a, b, c, t = symbols('a b c t')
    vt = Matrix([a*t, b, c])
    assert integrate(vt, t) == Integral(vt, t).doit()
    assert integrate(vt, t) == Matrix([[a*t**2/2], [b*t], [c*t]])

