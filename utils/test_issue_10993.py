
def test_issue_10993():
    assert solve(Eq(binomial(x, 2), 3)) == [-2, 3]
    assert solve(Eq(pow(x, 2) + binomial(x, 3), x)) == [-4, 0, 1]
    assert solve(Eq(binomial(x, 2), 0)) == [0, 1]
    assert solve(a+binomial(x, 3), a) == [-binomial(x, 3)]
    assert solve(x-binomial(a, 3) + binomial(y, 2) + sin(a), x) == [-sin(a) + binomial(a, 3) - binomial(y, 2)]
    assert solve((x+1)-binomial(x+1, 3), x) == [-2, -1, 3]

