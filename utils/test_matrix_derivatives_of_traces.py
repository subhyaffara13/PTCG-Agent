
def test_matrix_derivatives_of_traces():

    expr = Trace(A)*A
    I = Identity(k)
    assert expr.diff(A) == ArrayAdd(ArrayTensorProduct(I, A), PermuteDims(ArrayTensorProduct(Trace(A)*I, I), Permutation(3)(1, 2)))
    assert expr[i, j].diff(A[m, n]).doit() == (
        KDelta(i, m)*KDelta(j, n)*Trace(A) +
        KDelta(m, n)*A[i, j]
    )

    ## First order:

    # Cookbook example 99:
    expr = Trace(X)
    assert expr.diff(X) == Identity(k)
    assert expr.rewrite(Sum).diff(X[m, n]).doit() == KDelta(m, n)

    # Cookbook example 100:
    expr = Trace(X*A)
    assert expr.diff(X) == A.T
    assert expr.rewrite(Sum).diff(X[m, n]).doit() == A[n, m]

    # Cookbook example 101:
    expr = Trace(A*X*B)
    assert expr.diff(X) == A.T*B.T
    assert expr.rewrite(Sum).diff(X[m, n]).doit().dummy_eq((A.T*B.T)[m, n])

    # Cookbook example 102:
    expr = Trace(A*X.T*B)
    assert expr.diff(X) == B*A

    # Cookbook example 103:
    expr = Trace(X.T*A)
    assert expr.diff(X) == A

    # Cookbook example 104:
    expr = Trace(A*X.T)
    assert expr.diff(X) == A

    # Cookbook example 105:
    # TODO: TensorProduct is not supported
    #expr = Trace(TensorProduct(A, X))
    #assert expr.diff(X) == Trace(A)*Identity(k)

    ## Second order:

    # Cookbook example 106:
    expr = Trace(X**2)
    assert expr.diff(X) == 2*X.T

    # Cookbook example 107:
    expr = Trace(X**2*B)
    assert expr.diff(X) == (X*B + B*X).T
    expr = Trace(MatMul(X, X, B))
    assert expr.diff(X) == (X*B + B*X).T

    # Cookbook example 108:
    expr = Trace(X.T*B*X)
    assert expr.diff(X) == B*X + B.T*X

    # Cookbook example 109:
    expr = Trace(B*X*X.T)
    assert expr.diff(X) == B*X + B.T*X

    # Cookbook example 110:
    expr = Trace(X*X.T*B)
    assert expr.diff(X) == B*X + B.T*X

    # Cookbook example 111:
    expr = Trace(X*B*X.T)
    assert expr.diff(X) == X*B.T + X*B

    # Cookbook example 112:
    expr = Trace(B*X.T*X)
    assert expr.diff(X) == X*B.T + X*B

    # Cookbook example 113:
    expr = Trace(X.T*X*B)
    assert expr.diff(X) == X*B.T + X*B

    # Cookbook example 114:
    expr = Trace(A*X*B*X)
    assert expr.diff(X) == A.T*X.T*B.T + B.T*X.T*A.T

    # Cookbook example 115:
    expr = Trace(X.T*X)
    assert expr.diff(X) == 2*X
    expr = Trace(X*X.T)
    assert expr.diff(X) == 2*X

    # Cookbook example 116:
    expr = Trace(B.T*X.T*C*X*B)
    assert expr.diff(X) == C.T*X*B*B.T + C*X*B*B.T

    # Cookbook example 117:
    expr = Trace(X.T*B*X*C)
    assert expr.diff(X) == B*X*C + B.T*X*C.T

    # Cookbook example 118:
    expr = Trace(A*X*B*X.T*C)
    assert expr.diff(X) == A.T*C.T*X*B.T + C*A*X*B

    # Cookbook example 119:
    expr = Trace((A*X*B + C)*(A*X*B + C).T)
    assert expr.diff(X) == 2*A.T*(A*X*B + C)*B.T

    # Cookbook example 120:
    # TODO: no support for TensorProduct.
    # expr = Trace(TensorProduct(X, X))
    # expr = Trace(X)*Trace(X)
    # expr.diff(X) == 2*Trace(X)*Identity(k)

    # Higher Order

    # Cookbook example 121:
    expr = Trace(X**k)
    #assert expr.diff(X) == k*(X**(k-1)).T

    # Cookbook example 122:
    expr = Trace(A*X**k)
    #assert expr.diff(X) == # Needs indices

    # Cookbook example 123:
    expr = Trace(B.T*X.T*C*X*X.T*C*X*B)
    assert expr.diff(X) == C*X*X.T*C*X*B*B.T + C.T*X*B*B.T*X.T*C.T*X + C*X*B*B.T*X.T*C*X + C.T*X*X.T*C.T*X*B*B.T

    # Other

    # Cookbook example 124:
    expr = Trace(A*X**(-1)*B)
    assert expr.diff(X) == -Inverse(X).T*A.T*B.T*Inverse(X).T

    # Cookbook example 125:
    expr = Trace(Inverse(X.T*C*X)*A)
    # Warning: result in the cookbook is equivalent if B and C are symmetric:
    assert expr.diff(X) == - X.inv().T*A.T*X.inv()*C.inv().T*X.inv().T - X.inv().T*A*X.inv()*C.inv()*X.inv().T

    # Cookbook example 126:
    expr = Trace((X.T*C*X).inv()*(X.T*B*X))
    assert expr.diff(X) == -2*C*X*(X.T*C*X).inv()*X.T*B*X*(X.T*C*X).inv() + 2*B*X*(X.T*C*X).inv()

    # Cookbook example 127:
    expr = Trace((A + X.T*C*X).inv()*(X.T*B*X))
    # Warning: result in the cookbook is equivalent if B and C are symmetric:
    assert expr.diff(X) == B*X*Inverse(A + X.T*C*X) - C*X*Inverse(A + X.T*C*X)*X.T*B*X*Inverse(A + X.T*C*X) - C.T*X*Inverse(A.T + (C*X).T*X)*X.T*B.T*X*Inverse(A.T + (C*X).T*X) + B.T*X*Inverse(A.T + (C*X).T*X)

