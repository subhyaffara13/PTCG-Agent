
def test__unevaluated_Mul():
    A, B = symbols('A B', commutative=False)
    assert _unevaluated_Mul(x, A, B, S(2), A).args == (2, x, A, B, A)
    assert _unevaluated_Mul(-x*A*B, S(2), A).args == (-2, x, A, B, A)

