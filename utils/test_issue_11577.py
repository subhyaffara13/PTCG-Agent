
def test_issue_11577():
    def check(eq):
        r, c = cse(eq)
        assert eq.count_ops() >= \
            len(r) + sum(i[1].count_ops() for i in r) + \
            count_ops(c)

    eq = x**5*y**2 + x**5*y + x**5
    assert cse(eq) == (
        [(x0, x**4), (x1, x*y)], [x**5 + x0*x1*y + x0*x1])
        # ([(x0, x**5*y)], [x0*y + x0 + x**5]) or
        # ([(x0, x**5)], [x0*y**2 + x0*y + x0])
    check(eq)

    eq = x**2/(y + 1)**2 + x/(y + 1)
    assert cse(eq) == (
        [(x0, y + 1)], [x**2/x0**2 + x/x0])
        # ([(x0, x/(y + 1))], [x0**2 + x0])
    check(eq)

