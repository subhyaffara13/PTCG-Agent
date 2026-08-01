
def test_matrix_derivative_vectors_and_scalars():

    assert x.diff(x) == Identity(k)
    assert x[i, 0].diff(x[m, 0]).doit() == KDelta(m, i)

    assert x.T.diff(x) == Identity(k)

    # Cookbook example 69:
    expr = x.T*a
    assert expr.diff(x) == a
    assert expr[0, 0].diff(x[m, 0]).doit() == a[m, 0]
    expr = a.T*x
    assert expr.diff(x) == a

    # Cookbook example 70:
    expr = a.T*X*b
    assert expr.diff(X) == a*b.T

    # Cookbook example 71:
    expr = a.T*X.T*b
    assert expr.diff(X) == b*a.T

    # Cookbook example 72:
    expr = a.T*X*a
    assert expr.diff(X) == a*a.T
    expr = a.T*X.T*a
    assert expr.diff(X) == a*a.T

    # Cookbook example 77:
    expr = b.T*X.T*X*c
    assert expr.diff(X) == X*b*c.T + X*c*b.T

    # Cookbook example 78:
    expr = (B*x + b).T*C*(D*x + d)
    assert expr.diff(x) == B.T*C*(D*x + d) + D.T*C.T*(B*x + b)

    # Cookbook example 81:
    expr = x.T*B*x
    assert expr.diff(x) == B*x + B.T*x

    # Cookbook example 82:
    expr = b.T*X.T*D*X*c
    assert expr.diff(X) == D.T*X*b*c.T + D*X*c*b.T

    # Cookbook example 83:
    expr = (X*b + c).T*D*(X*b + c)
    assert expr.diff(X) == D*(X*b + c)*b.T + D.T*(X*b + c)*b.T
    assert str(expr[0, 0].diff(X[m, n]).doit()) == \
        'b[n, 0]*Sum((c[_i_1, 0] + Sum(X[_i_1, _i_3]*b[_i_3, 0], (_i_3, 0, k - 1)))*D[_i_1, m], (_i_1, 0, k - 1)) + Sum((c[_i_2, 0] + Sum(X[_i_2, _i_4]*b[_i_4, 0], (_i_4, 0, k - 1)))*D[m, _i_2]*b[n, 0], (_i_2, 0, k - 1))'

    # See https://github.com/sympy/sympy/issues/16504#issuecomment-1018339957
    expr = x*x.T*x
    I = Identity(k)
    assert expr.diff(x) == KroneckerProduct(I, x.T*x) + 2*x*x.T

