
def test_issue_4463():
    assert solve(-a*x + 2*x*log(x), x) == [exp(a/2)]
    assert solve(x**x) == []
    assert solve(x**x - 2) == [exp(LambertW(log(2)))]
    assert solve(((x - 3)*(x - 2))**((x - 3)*(x - 4))) == [2]

