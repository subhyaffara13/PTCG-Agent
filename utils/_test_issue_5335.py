
def _test_issue_5335():
    # Not able to check zero dimensional system.
    # is_zero_dimensional Hangs
    lam, a0, conc = symbols('lam a0 conc')
    eqs = [lam + 2*y - a0*(1 - x/2)*x - 0.005*x/2*x,
           a0*(1 - x/2)*x - 1*y - 0.743436700916726*y,
           x + y - conc]
    sym = [x, y, a0]
    # there are 4 solutions but only two are valid
    assert len(nonlinsolve(eqs, sym)) == 2
    # float
    eqs = [lam + 2*y - a0*(1 - x/2)*x - 0.005*x/2*x,
           a0*(1 - x/2)*x - 1*y - 0.743436700916726*y,
           x + y - conc]
    sym = [x, y, a0]
    assert len(nonlinsolve(eqs, sym)) == 2

