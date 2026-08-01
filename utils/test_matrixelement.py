
def test_matrixelement():
    x = MatrixSymbol('x', 3, 3)
    i = Symbol('i', positive = True)
    j = Symbol('j', positive = True)
    assert refine(x[0, 1], Q.symmetric(x)) == x[0, 1]
    assert refine(x[1, 0], Q.symmetric(x)) == x[0, 1]
    assert refine(x[i, j], Q.symmetric(x)) == x[j, i]
    assert refine(x[j, i], Q.symmetric(x)) == x[j, i]

