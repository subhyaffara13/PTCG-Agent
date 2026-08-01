
def test_sign2():
    assert sign(x, x) == 1
    assert sign(-x, x) == -1
    y = Symbol("y", positive=True)
    assert sign(y, x) == 1
    assert sign(-y, x) == -1
    assert sign(y*x, x) == 1
    assert sign(-y*x, x) == -1

