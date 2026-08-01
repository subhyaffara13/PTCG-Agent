
def test_issue_5183():
    # using list(...) so py.test can recalculate values
    tests = list(product([x, -x],
                         [-1, 1],
                         [2, 3, S.Half, Rational(2, 3)],
                         ['-', '+']))
    results = (oo, oo, -oo, oo, -oo*I, oo, -oo*(-1)**Rational(1, 3), oo,
               0, 0, 0, 0, 0, 0, 0, 0,
               oo, oo, oo, -oo, oo, -oo*I, oo, -oo*(-1)**Rational(1, 3),
               0, 0, 0, 0, 0, 0, 0, 0)
    assert len(tests) == len(results)
    for i, (args, res) in enumerate(zip(tests, results)):
        y, s, e, d = args
        eq = y**(s*e)
        try:
            assert limit(eq, x, 0, dir=d) == res
        except AssertionError:
            if 0:  # change to 1 if you want to see the failing tests
                print()
                print(i, res, eq, d, limit(eq, x, 0, dir=d))
            else:
                assert None


def test_issue_5183():
    s = (x + 1/x).lseries()
    assert list(s) == [1/x, x]
    assert next((x + x**2).lseries()) == x
    assert next(((1 + x)**7).lseries(x)) == 1
    assert next((sin(x + y)).series(x, n=3).lseries(y)) == x
    # it would be nice if all terms were grouped, but in the
    # following case that would mean that all the terms would have
    # to be known since, for example, every term has a constant in it.
    s = ((1 + x)**7).series(x, 1, n=None)
    assert [next(s) for i in range(2)] == [128, -448 + 448*x]


def test_issue_5183():
    assert abs(x + x**2).series(n=1) == O(x)
    assert abs(x + x**2).series(n=2) == x + O(x**2)
    assert ((1 + x)**2).series(x, n=6) == x**2 + 2*x + 1
    assert (1 + 1/x).series() == 1 + 1/x
    assert Derivative(exp(x).series(), x).doit() == \
        1 + x + x**2/2 + x**3/6 + x**4/24 + O(x**5)

