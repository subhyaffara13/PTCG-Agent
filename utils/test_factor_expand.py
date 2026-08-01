
def test_factor_expand():
    A = MatrixSymbol("A", n, n)
    B = MatrixSymbol("B", n, n)
    expr1 = (A + B)*(C + D)
    expr2 = A*C + B*C + A*D + B*D
    assert expr1 != expr2
    assert expand(expr1) == expr2
    assert factor(expr2) == expr1

    expr = B**(-1)*(A**(-1)*B**(-1) - A**(-1)*C*B**(-1))**(-1)*A**(-1)
    I = Identity(n)
    # Ideally we get the first, but we at least don't want a wrong answer
    assert factor(expr) in [I - C, B**-1*(A**-1*(I - C)*B**-1)**-1*A**-1]

