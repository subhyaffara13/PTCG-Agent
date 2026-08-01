
def test_issue_4376():
    n = Symbol('n', integer=True, positive=True)
    assert simplify(integrate(n*(x**(1/n) - 1), (x, 0, S.Half)) -
                (n**2 - 2**(1/n)*n**2 - n*2**(1/n))/(2**(1 + 1/n) + n*2**(1 + 1/n))) == 0

