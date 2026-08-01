
def test_O1():
    M = Matrix((1 + I, -2, 3*I))
    assert sqrt(expand(M.dot(M.H))) == sqrt(15)


def test_O1():
    assert O(1, x) * x == O(x)
    assert O(1, y) * x == O(1, y)

