
def test_issue_8697():
    a = Function('a')
    eq = a(n + 3) - a(n + 2) - a(n + 1) + a(n)
    assert rsolve(eq, a(n)) == (-1)**n*C1 + C0 + C2*n
    eq2 = a(n + 3) + 3*a(n + 2) + 3*a(n + 1) + a(n)
    assert (rsolve(eq2, a(n)) ==
            (-1)**n*C0 + (-1)**(n + 1)*C1*n + (-1)**(n + 1)*C2*n**2)

    assert rsolve(a(n) - 2*a(n - 3) + 5*a(n - 2) - 4*a(n - 1),
                  a(n), {a(0): 1, a(1): 3, a(2): 8}) == 3*2**n - n - 2

    # From issue thread (but fixed by https://github.com/diofant/diofant/commit/da9789c6cd7d0c2ceeea19fbf59645987125b289):
    assert rsolve(a(n) - 2*a(n - 1) - n, a(n), {a(0): 1}) == 3*2**n - n - 2

