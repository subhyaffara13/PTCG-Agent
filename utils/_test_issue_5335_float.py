
def _test_issue_5335_float():
    # gives ZeroDivisionError: polynomial division
    lam, a0, conc = symbols('lam a0 conc')
    a = 0.005
    b = 0.743436700916726
    eqs = [lam + 2*y - a0*(1 - x/2)*x - a*x/2*x,
           a0*(1 - x/2)*x - 1*y - b*y,
           x + y - conc]
    sym = [x, y, a0]
    assert len(solve(eqs, sym, rational=False)) == 2

