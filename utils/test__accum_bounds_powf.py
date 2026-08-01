
def test_AccumBounds_powf():
    nn = Symbol('nn', nonnegative=True)
    assert B(1 + nn, 2 + nn)**B(1, 2) == B(1 + nn, (2 + nn)**2)
    i = Symbol('i', integer=True, negative=True)
    assert B(1, 2)**i == B(2**i, 1)

