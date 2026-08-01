
def test_issue_20747():
    THT, HT, DBH, dib, c0, c1, c2, c3, c4  = symbols('THT HT DBH dib c0 c1 c2 c3 c4')
    f = DBH*c3 + THT*c4 + c2
    rhs = 1 - ((HT - 1)/(THT - 1))**c1*(1 - exp(c0/f))
    eq = dib - DBH*(c0 - f*log(rhs))
    term = ((1 - exp((DBH*c0 - dib)/(DBH*(DBH*c3 + THT*c4 + c2))))
            / (1 - exp(c0/(DBH*c3 + THT*c4 + c2))))
    sol = [THT*term**(1/c1) - term**(1/c1) + 1]
    assert solve(eq, HT) == sol

