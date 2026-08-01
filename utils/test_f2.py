
def test_F2():
    assert expand_func(binomial(n, 3)) == n*(n - 1)*(n - 2)/6


def test_f2():
    assert limit((sqrt(
        cos(x)) - root3(cos(x)))/(sin(x)**2), x, 0) == -Rational(1, 12)  # *184


def test_f2():
    assert bool(dpll_satisfiable(load(f2)))

