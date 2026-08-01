
def test_relational_arithmetic():
    for cls in [Eq, Ne, Le, Lt, Ge, Gt]:
        rel = cls(x, y)
        raises(TypeError, lambda: 0+rel)
        raises(TypeError, lambda: 1*rel)
        raises(TypeError, lambda: 1**rel)
        raises(TypeError, lambda: rel**1)
        raises(TypeError, lambda: Add(0, rel))
        raises(TypeError, lambda: Mul(1, rel))
        raises(TypeError, lambda: Pow(1, rel))
        raises(TypeError, lambda: Pow(rel, 1))

