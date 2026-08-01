
def test_P13():
    M = Matrix([[1,     x - 2,                         x - 3],
                [x - 1, x**2 - 3*x + 6,       x**2 - 3*x - 2],
                [x - 2, x**2 - 8,       2*(x**2) - 12*x + 14]])
    L, U, _ = M.LUdecomposition()
    assert simplify(L) == Matrix([[1,     0,     0],
                                  [x - 1, 1,     0],
                                  [x - 2, x - 3, 1]])
    assert simplify(U) == Matrix([[1, x - 2, x - 3],
                                  [0,     4, x - 5],
                                  [0,     0, x - 7]])

