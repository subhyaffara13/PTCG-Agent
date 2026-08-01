
def test_Z2():
    r = Function('r')
    assert (rsolve(r(n) - (5*r(n - 1) - 6*r(n - 2)), r(n), {r(0): 0, r(1): 1})
            == -2**n + 3**n)

