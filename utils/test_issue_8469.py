
def test_issue_8469():
    # This should not take forever to run
    N = 40
    def g(w, theta):
        return 1/(1+exp(w-theta))

    ws = symbols(['w%i'%i for i in range(N)])
    import functools
    expr = functools.reduce(g, ws)
    assert isinstance(expr, Pow)

