
def test_FracField_index():
    a = symbols("a")
    F, x, y, z = field('x y z', QQ)
    assert F.index(x) == 0
    assert F.index(y) == 1

    raises(ValueError, lambda: F.index(1))
    raises(ValueError, lambda: F.index(a))
    pass

