
def test_issue_5335():
    lam, a0, conc = symbols('lam a0 conc')
    a = 0.005
    b = 0.743436700916726
    eqs = [lam + 2*y - a0*(1 - x/2)*x - a*x/2*x,
           a0*(1 - x/2)*x - 1*y - b*y,
           x + y - conc]
    sym = [x, y, a0]
    # there are 4 solutions obtained manually but only two are valid
    assert len(solve(eqs, sym, manual=True, minimal=True)) == 2
    assert len(solve(eqs, sym)) == 2  # cf below with rational=False

