
def test_lpmin_lpmax():
    v = x1, x2, y1, y2 = symbols('x1 x2 y1 y2')
    L = [[1, -1]], [1], [[1, 1]], [2]
    a, b, c, d = [Matrix(i) for i in L]
    m = Matrix([[a, b], [c, d]])
    f, constr = _primal_dual(m)[0]
    ans = lpmin(f, constr + [i >= 0 for i in v[:2]])
    assert ans == (-1, {x1: 1, x2: 0}),ans

    L = [[1, -1], [1, 1]], [1, 1], [[1, 1]], [2]
    a, b, c, d = [Matrix(i) for i in L]
    m = Matrix([[a, b], [c, d]])
    f, constr = _primal_dual(m)[1]
    ans = lpmax(f, constr + [i >= 0 for i in v[-2:]])
    assert ans == (-1, {y1: 1, y2: 0})

