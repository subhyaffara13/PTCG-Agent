
def test_block_matrix_derivative():
    x = symbols('x')
    A = Matrix(3, 3, [Function(f'a{i}')(x) for i in range(9)])
    bc = BlockMatrix([[A[:2, :2], A[:2, 2]], [A[2, :2], A[2:, 2]]])
    assert Matrix(bc.diff(x)) - A.diff(x) == zeros(3, 3)

