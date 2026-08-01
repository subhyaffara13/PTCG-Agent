
def test_issue_21942():
    eq = -d + (a*c**(1 - e) + b**(1 - e)*(1 - a))**(1/(1 - e))
    sol = solve(eq, c, simplify=False, check=False)
    assert sol == [((a*b**(1 - e) - b**(1 - e) +
        d**(1 - e))/a)**(1/(1 - e))]

