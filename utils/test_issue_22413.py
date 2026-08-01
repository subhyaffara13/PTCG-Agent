
def test_issue_22413():
    res =  nonlinsolve((4*y*(2*x + 2*exp(y) + 1)*exp(2*x),
                         4*x*exp(2*x) + 4*y*exp(2*x + y) + 4*exp(2*x + y) + 1),
                        x, y)
    # First solution is not correct, but the issue was an exception
    sols = FiniteSet((x, S.Zero), (-exp(y) - S.Half, y))
    assert res == sols

