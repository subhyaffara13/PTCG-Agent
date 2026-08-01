
def test_H15():
    assert simplify(Mul(*[x - r for r in solveset(x**3 + x**2 - 7)])) == x**3 + x**2 - 7

