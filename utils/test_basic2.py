
def test_basic2():
    assert limit(x**x, x, 0, dir="+") == 1
    assert limit((exp(x) - 1)/x, x, 0) == 1
    assert limit(1 + 1/x, x, oo) == 1
    assert limit(-exp(1/x), x, oo) == -1
    assert limit(x + exp(-x), x, oo) is oo
    assert limit(x + exp(-x**2), x, oo) is oo
    assert limit(x + exp(-exp(x)), x, oo) is oo
    assert limit(13 + 1/x - exp(-x), x, oo) == 13


def test_basic2():
    assert residue(1/x, x, 1) == 0
    assert residue(-2/x, x, 1) == 0
    assert residue(81/x, x, -1) == 0
    assert residue(1/x**2, x, 1) == 0
    assert residue(0, x, 1) == 0
    assert residue(5, x, 1) == 0
    assert residue(x, x, 1) == 0
    assert residue(x**2, x, 5) == 0

