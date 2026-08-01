
def test_issue_14528():
    p = symbols("p", integer=True, positive=True)
    assert combsimp(binomial(1,p)) == 1/(factorial(p)*factorial(1-p))
    assert combsimp(factorial(2-p)) == factorial(2-p)


def test_issue_14528():
    k = Symbol('k', integer=True, nonpositive=True)
    assert isinstance(gamma(k), gamma)

