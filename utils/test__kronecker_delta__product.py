
def test_KroneckerDelta_Product():
    y = Symbol('y')
    assert Product(x*KroneckerDelta(x, y), (x, 0, 1)).doit() == 0

