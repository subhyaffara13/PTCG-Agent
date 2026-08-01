
def test_issue_21176():
    f = x**2*cot(pi*x)/(x**4 + 1)
    assert residue(f, x, -sqrt(2)/2 - sqrt(2)*I/2).cancel().together(deep=True)\
        == sqrt(2)*(1 - I)/(8*tan(sqrt(2)*pi*(1 + I)/2))

