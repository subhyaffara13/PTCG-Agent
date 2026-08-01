
def test_issue_18153():
    assert integrate(x**n*log(x),x) == \
    Piecewise(
        (n*x*x**n*log(x)/(n**2 + 2*n + 1) +
    x*x**n*log(x)/(n**2 + 2*n + 1) - x*x**n/(n**2 + 2*n + 1)
    , Ne(n, -1)), (log(x)**2/2, True)
    )

