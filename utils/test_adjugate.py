
def test_adjugate():
    x = Symbol('x')
    e = Matrix(4, 4,
        [x, 1, 2, 3, 4, 5, 6, 7, 2, 9, 10, 11, 12, 13, 14, 14])

    adj = Matrix([
        [   4,         -8,         4,         0],
        [  76, -14*x - 68,  14*x - 8, -4*x + 24],
        [-122, 17*x + 142, -21*x + 4,  8*x - 48],
        [  48,  -4*x - 72,       8*x, -4*x + 24]])
    assert e.adjugate() == adj
    assert e.adjugate(method='bareiss') == adj
    assert e.adjugate(method='berkowitz') == adj
    assert e.adjugate(method='bird') == adj
    assert e.adjugate(method='laplace') == adj

    a = Matrix(2, 3, [1, 2, 3, 4, 5, 6])
    raises(NonSquareMatrixError, lambda: a.adjugate())

