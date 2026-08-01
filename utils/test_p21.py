
def test_P21():
    M = Matrix([[5, -3, -7],
                [-2, 1,  2],
                [2, -3, -4]])
    assert M.charpoly(x).as_expr() == x**3 - 2*x**2 - 5*x + 6

