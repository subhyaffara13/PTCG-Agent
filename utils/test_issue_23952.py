
def test_issue_23952():
    assert (x**(y + z)).expand(force=True) == x**y*x**z
    one = Symbol('1', integer=True, prime=True, odd=True, positive=True)
    two = Symbol('2', integer=True, prime=True, even=True)
    e = two - one
    for b in (0, x):
        # 0**e = 0, 0**-e = zoo; but if expanded then nan
        assert unchanged(Pow, b, e)  # power_exp
        assert unchanged(Pow, b, -e)  # power_exp
        assert unchanged(Pow, b, y - x)  # power_exp
        assert unchanged(Pow, b, 3 - x)  # multinomial
        assert (b**e).expand().is_Pow  # power_exp
        assert (b**-e).expand().is_Pow  # power_exp
        assert (b**(y - x)).expand().is_Pow  # power_exp
        assert (b**(3 - x)).expand().is_Pow  # multinomial
    nn1 = Symbol('nn1', nonnegative=True)
    nn2 = Symbol('nn2', nonnegative=True)
    nn3 = Symbol('nn3', nonnegative=True)
    assert (x**(nn1 + nn2)).expand() == x**nn1*x**nn2
    assert (x**(-nn1 - nn2)).expand() == x**-nn1*x**-nn2
    assert unchanged(Pow, x, nn1 + nn2 - nn3)
    assert unchanged(Pow, x, 1 + nn2 - nn3)
    assert unchanged(Pow, x, nn1 - nn2)
    assert unchanged(Pow, x, 1 - nn2)
    assert unchanged(Pow, x, -1 + nn2)


def test_issue_23952():
    p, q = symbols("p q", real=True, nonnegative=True)
    k1, k2 = symbols("k1 k2", integer=True, nonnegative=True)
    n = Symbol("n", integer=True, positive=True)
    expr = Sum(abs(k1 - k2)*p**k1 *(1 - q)**(n - k2),
        (k1, 0, n), (k2, 0, n))
    assert expr.subs(p,0).subs(q,1).subs(n, 3).doit() == 3

