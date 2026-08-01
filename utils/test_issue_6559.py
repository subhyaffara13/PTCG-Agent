
def test_issue_6559():
    assert (-12*x + y).subs(-x, 1) == 12 + y
    # though this involves cse it generated a failure in Mul._eval_subs
    x0, x1 = symbols('x0 x1')
    e = -log(-12*sqrt(2) + 17)/24 - log(-2*sqrt(2) + 3)/12 + sqrt(2)/3
    # XXX modify cse so x1 is eliminated and x0 = -sqrt(2)?
    assert cse(e) == (
        [(x0, sqrt(2))], [x0/3 - log(-12*x0 + 17)/24 - log(-2*x0 + 3)/12])

