
def test_issue_11004():

    def f(n):
        return sqrt(2*pi*n) * (n/E)**n

    def m(n, k):
        return  f(n) / (f(n/k)**k)

    def p(n,k):
        return m(n, k) / (k**n)

    N, k = symbols('N k')
    half = Float('0.5', 4)
    z = log(p(n, k) / p(n, k + 1)).expand(force=True)
    r = simplify(z.subs(n, N).n(4))
    assert r == (
        half*k*log(k)
        - half*k*log(k + 1)
        + half*log(N)
        - half*log(k + 1)
        + Float(0.9189224, 4)
    )

