
def test_issue_4546():
    # using list(...) so py.test can recalculate values
    tests = list(product([cot, tan],
                         [-pi/2, 0, pi/2, pi, pi*Rational(3, 2)],
                         ['-', '+']))
    results = (0, 0, -oo, oo, 0, 0, -oo, oo, 0, 0,
               oo, -oo, 0, 0, oo, -oo, 0, 0, oo, -oo)
    assert len(tests) == len(results)
    for i, (args, res) in enumerate(zip(tests, results)):
        f, l, d = args
        eq = f(x)
        try:
            assert limit(eq, x, l, dir=d) == res
        except AssertionError:
            if 0:  # change to 1 if you want to see the failing tests
                print()
                print(i, res, eq, l, d, limit(eq, x, l, dir=d))
            else:
                assert None

