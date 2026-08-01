
def test_issue_15925b_manual():
    assert not integrate(sqrt((-12*cos(x)**2*sin(x))**2+(12*cos(x)*sin(x)**2)**2),
                         (x, 0, pi/6), manual=True).has(Integral)

