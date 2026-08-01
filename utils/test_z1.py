
def test_Z1():
    r = Function('r')
    assert (rsolve(r(n + 2) - 2*r(n + 1) + r(n) - 2, r(n),
                   {r(0): 1, r(1): m}).simplify() == n**2 + n*(m - 2) + 1)

