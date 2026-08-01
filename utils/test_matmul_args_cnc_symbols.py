
def test_matmul_args_cnc_symbols():
    # Not currently supported
    a, b = symbols('a b', commutative=False)
    assert MatMul(n, a, b, A, A.T).args_cnc() == [[n], [a, b, A, A.T]]
    assert MatMul(n, a, A, b, A.T).args_cnc() == [[n], [a, A, b, A.T]]

