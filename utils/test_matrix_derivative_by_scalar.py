
def test_matrix_derivative_by_scalar():
    assert A.diff(i) == ZeroMatrix(k, k)
    assert (A*(X + B)*c).diff(i) == ZeroMatrix(k, 1)
    assert x.diff(i) == ZeroMatrix(k, 1)
    assert (x.T*y).diff(i) == ZeroMatrix(1, 1)
    assert (x*x.T).diff(i) == ZeroMatrix(k, k)
    assert (x + y).diff(i) == ZeroMatrix(k, 1)
    assert hadamard_power(x, 2).diff(i) == ZeroMatrix(k, 1)
    assert hadamard_power(x, i).diff(i).dummy_eq(
        HadamardProduct(x.applyfunc(log), HadamardPower(x, i)))
    assert hadamard_product(x, y).diff(i) == ZeroMatrix(k, 1)
    assert hadamard_product(i*OneMatrix(k, 1), x, y).diff(i) == hadamard_product(x, y)
    assert (i*x).diff(i) == x
    assert (sin(i)*A*B*x).diff(i) == cos(i)*A*B*x
    assert x.applyfunc(sin).diff(i) == ZeroMatrix(k, 1)
    assert Trace(i**2*X).diff(i) == 2*i*Trace(X)

    mu = symbols("mu")
    expr = (2*mu*x)
    assert expr.diff(x) == 2*mu*Identity(k)

