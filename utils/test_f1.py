
def test_F1():
    assert rf(x, 3) == x*(1 + x)*(2 + x)


def test_f1():
    assert bool(dpll_satisfiable(load(f1)))

