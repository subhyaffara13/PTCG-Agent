
def test_F4():
    assert combsimp(2**n * factorial(n) * product(2*k - 1, (k, 1, n))) == factorial(2*n)


def test_f4():
    assert not bool(dpll_satisfiable(load(f4)))

