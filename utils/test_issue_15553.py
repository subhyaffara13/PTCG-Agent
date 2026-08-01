
def test_issue_15553():
    f = Function("f")
    assert rsolve(Eq(f(n), 2*f(n - 1) + n), f(n)) == 2**n*C0 - n - 2
    assert rsolve(Eq(f(n + 1), 2*f(n) + n**2 + 1), f(n)) == 2**n*C0 - n**2 - 2*n - 4
    assert rsolve(Eq(f(n + 1), 2*f(n) + n**2 + 1), f(n), {f(1): 0}) == 7*2**n/2 - n**2 - 2*n - 4
    assert rsolve(Eq(f(n), 2*f(n - 1) + 3*n**2), f(n)) == 2**n*C0 - 3*n**2 - 12*n - 18
    assert rsolve(Eq(f(n), 2*f(n - 1) + n**2), f(n)) == 2**n*C0 - n**2 - 4*n - 6
    assert rsolve(Eq(f(n), 2*f(n - 1) + n), f(n), {f(0): 1}) == 3*2**n - n - 2

