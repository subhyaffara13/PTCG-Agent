
def test_issue_21195():
    t = symbols('t')
    x = Function('x')(t)
    dx = x.diff(t)
    exp1 = cos(x) + cos(x)*dx
    exp2 = sin(x) + tan(x)*(dx.diff(t))
    exp3 = sin(x)*sin(t)*(dx.diff(t)).diff(t)
    A = Matrix([[exp1], [exp2], [exp3]])
    B = Matrix([[exp1.diff(x)], [exp2.diff(x)], [exp3.diff(x)]])
    assert A.diff(x) == B

