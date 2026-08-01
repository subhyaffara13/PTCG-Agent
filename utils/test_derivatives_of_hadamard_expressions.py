
def test_derivatives_of_hadamard_expressions():

    # Hadamard Product

    expr = hadamard_product(a, x, b)
    assert expr.diff(x) == DiagMatrix(hadamard_product(b, a))

    expr = a.T*hadamard_product(A, X, B)*b
    assert expr.diff(X) == HadamardProduct(a*b.T, A, B)

    # Hadamard Power

    expr = hadamard_power(x, 2)
    assert expr.diff(x).doit() == 2*DiagMatrix(x)

    expr = hadamard_power(x.T, 2)
    assert expr.diff(x).doit() == 2*DiagMatrix(x)

    expr = hadamard_power(x, S.Half)
    assert expr.diff(x) == S.Half*DiagMatrix(hadamard_power(x, Rational(-1, 2)))

    expr = hadamard_power(a.T*X*b, 2)
    assert expr.diff(X) == 2*a*a.T*X*b*b.T

    expr = hadamard_power(a.T*X*b, S.Half)
    assert expr.diff(X) == a/(2*sqrt(a.T*X*b))*b.T

