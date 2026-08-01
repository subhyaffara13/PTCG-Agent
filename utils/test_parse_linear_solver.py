
def test_parse_linear_solver():
    A, b = Matrix(3, 3, symbols('a:9')), Matrix(3, 2, symbols('b:6'))
    assert _parse_linear_solver(Matrix.LUsolve) == Matrix.LUsolve  # Test callable
    assert _parse_linear_solver('LU')(A, b) == Matrix.LUsolve(A, b)

