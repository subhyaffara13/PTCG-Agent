
def test_issue_22689():
    assert str(Mul(Pow(x,-2, evaluate=False), Pow(3,-1,evaluate=False), evaluate=False)) == "1/(x**2*3)"

