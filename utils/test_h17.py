
def test_H17():
    assert simplify(factor(expand(p1 * p2)) - p1*p2) == 0

