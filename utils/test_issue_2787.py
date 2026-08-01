
def test_issue_2787():
    n, k = symbols('n k', positive=True, integer=True)
    p = symbols('p', positive=True)
    binomial_dist = binomial(n, k)*p**k*(1 - p)**(n - k)
    s = Sum(binomial_dist*k, (k, 0, n))
    res = s.doit().simplify()
    ans = Piecewise(
        (n*p, x),
        (Sum(k*p**k*binomial(n, k)*(1 - p)**(n - k), (k, 0, n)),
        True)).subs(x, (Eq(n, 1) | (n > 1)) & (p/Abs(p - 1) <= 1))
    ans2 = Piecewise(
        (n*p, x),
        (factorial(n)*Sum(p**k*(1 - p)**(-k + n)/
        (factorial(-k + n)*factorial(k - 1)), (k, 0, n)),
        True)).subs(x, (Eq(n, 1) | (n > 1)) & (p/Abs(p - 1) <= 1))
    assert res in [ans, ans2]  # XXX system dependent
    # Issue #17165: make sure that another simplify does not complicate
    # the result by much. Why didn't first simplify replace
    # Eq(n, 1) | (n > 1) with True?
    assert res.simplify().count_ops() <= res.count_ops() + 2

