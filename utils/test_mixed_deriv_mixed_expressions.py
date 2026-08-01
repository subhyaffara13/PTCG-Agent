
def test_mixed_deriv_mixed_expressions():

    expr = 3*Trace(A)
    assert expr.diff(A) == 3*Identity(k)

    expr = k
    deriv = expr.diff(A)
    assert isinstance(deriv, ZeroMatrix)
    assert deriv == ZeroMatrix(k, k)

    expr = Trace(A)**2
    assert expr.diff(A) == (2*Trace(A))*Identity(k)

    expr = Trace(A)*A
    I = Identity(k)
    assert expr.diff(A) == ArrayAdd(ArrayTensorProduct(I, A), PermuteDims(ArrayTensorProduct(Trace(A)*I, I), Permutation(3)(1, 2)))

    expr = Trace(Trace(A)*A)
    assert expr.diff(A) == (2*Trace(A))*Identity(k)

    expr = Trace(Trace(Trace(A)*A)*A)
    assert expr.diff(A) == (3*Trace(A)**2)*Identity(k)

