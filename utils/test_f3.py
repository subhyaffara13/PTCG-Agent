
def test_F3():
    assert combsimp(2**n * factorial(n) * factorial2(2*n - 1)) == factorial(2*n)


def test_f3():
    a = Symbol('a')
    #issue 3504
    assert limit(asin(a*x)/x, x, 0) == a


def test_f3():
    assert bool(dpll_satisfiable(load(f3)))

