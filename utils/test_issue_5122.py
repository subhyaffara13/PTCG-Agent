
def test_issue_5122():
    rng = np.random.default_rng(8312492117)
    p = 0
    n = rng.integers(100, size=10)

    x = 0
    ppf = binom.ppf(x, n, p)
    assert_equal(ppf, -1)

    x = np.linspace(0.01, 0.99, 10)
    ppf = binom.ppf(x, n, p)
    assert_equal(ppf, 0)

    x = 1
    ppf = binom.ppf(x, n, p)
    assert_equal(ppf, n)

