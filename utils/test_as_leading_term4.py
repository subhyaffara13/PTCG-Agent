
def test_as_leading_term4():
    # see issue 6843
    n = Symbol('n', integer=True, positive=True)
    r = -n**3/(2*n**2 + 4*n + 2) - n**2/(n**2 + 2*n + 1) + \
        n**2/(n + 1) - n/(2*n**2 + 4*n + 2) + n/(n*x + x) + 2*n/(n + 1) - \
        1 + 1/(n*x + x) + 1/(n + 1) - 1/x
    assert r.as_leading_term(x).cancel() == n/2

