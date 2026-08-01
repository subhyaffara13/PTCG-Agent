
def test_issue_17452():
    assert solve((7**x)**x + pi, x) == [-sqrt(log(pi) + I*pi)/sqrt(log(7)),
                                        sqrt(log(pi) + I*pi)/sqrt(log(7))]
    assert solve(x**(x/11) + pi/11, x) == [exp(LambertW(-11*log(11) + 11*log(pi) + 11*I*pi))]

