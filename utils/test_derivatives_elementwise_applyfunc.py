
def test_derivatives_elementwise_applyfunc():

    expr = x.applyfunc(tan)
    assert expr.diff(x).dummy_eq(
        DiagMatrix(x.applyfunc(lambda x: tan(x)**2 + 1)))
    assert expr[i, 0].diff(x[m, 0]).doit() == (tan(x[i, 0])**2 + 1)*KDelta(i, m)
    _check_derivative_with_explicit_matrix(expr, x, expr.diff(x))

    expr = (i**2*x).applyfunc(sin)
    assert expr.diff(i).dummy_eq(
        HadamardProduct((2*i)*x, (i**2*x).applyfunc(cos)))
    assert expr[i, 0].diff(i).doit() == 2*i*x[i, 0]*cos(i**2*x[i, 0])
    _check_derivative_with_explicit_matrix(expr, i, expr.diff(i))

    expr = (log(i)*A*B).applyfunc(sin)
    assert expr.diff(i).dummy_eq(
        HadamardProduct(A*B/i, (log(i)*A*B).applyfunc(cos)))
    _check_derivative_with_explicit_matrix(expr, i, expr.diff(i))

    expr = A*x.applyfunc(exp)
    # TODO: restore this result (currently returning the transpose):
    #  assert expr.diff(x).dummy_eq(DiagMatrix(x.applyfunc(exp))*A.T)
    _check_derivative_with_explicit_matrix(expr, x, expr.diff(x))

    expr = x.T*A*x + k*y.applyfunc(sin).T*x
    assert expr.diff(x).dummy_eq(A.T*x + A*x + k*y.applyfunc(sin))
    _check_derivative_with_explicit_matrix(expr, x, expr.diff(x))

    expr = x.applyfunc(sin).T*y
    # TODO: restore (currently returning the transpose):
    #  assert expr.diff(x).dummy_eq(DiagMatrix(x.applyfunc(cos))*y)
    _check_derivative_with_explicit_matrix(expr, x, expr.diff(x))

    expr = (a.T * X * b).applyfunc(sin)
    assert expr.diff(X).dummy_eq(a*(a.T*X*b).applyfunc(cos)*b.T)
    _check_derivative_with_explicit_matrix(expr, X, expr.diff(X))

    expr = a.T * X.applyfunc(sin) * b
    assert expr.diff(X).dummy_eq(
        DiagMatrix(a)*X.applyfunc(cos)*DiagMatrix(b))
    _check_derivative_with_explicit_matrix(expr, X, expr.diff(X))

    expr = a.T * (A*X*B).applyfunc(sin) * b
    assert expr.diff(X).dummy_eq(
        A.T*DiagMatrix(a)*(A*X*B).applyfunc(cos)*DiagMatrix(b)*B.T)
    _check_derivative_with_explicit_matrix(expr, X, expr.diff(X))

    expr = a.T * (A*X*b).applyfunc(sin) * b.T
    # TODO: not implemented
    #assert expr.diff(X) == ...
    #_check_derivative_with_explicit_matrix(expr, X, expr.diff(X))

    expr = a.T*A*X.applyfunc(sin)*B*b
    assert expr.diff(X).dummy_eq(
        HadamardProduct(A.T * a * b.T * B.T, X.applyfunc(cos)))

    expr = a.T * (A*X.applyfunc(sin)*B).applyfunc(log) * b
    # TODO: wrong
    # assert expr.diff(X) == A.T*DiagMatrix(a)*(A*X.applyfunc(sin)*B).applyfunc(Lambda(k, 1/k))*DiagMatrix(b)*B.T

    expr = a.T * (X.applyfunc(sin)).applyfunc(log) * b

