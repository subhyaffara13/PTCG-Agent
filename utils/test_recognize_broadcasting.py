
def test_recognize_broadcasting():
    expr = ArrayTensorProduct(x.T*x, A)
    assert _remove_trivial_dims(expr) == (KroneckerProduct(x.T*x, A), [0, 1])

    expr = ArrayTensorProduct(A, x.T*x)
    assert _remove_trivial_dims(expr) == (KroneckerProduct(A, x.T*x), [2, 3])

    expr = ArrayTensorProduct(A, B, x.T*x, C)
    assert _remove_trivial_dims(expr) == (ArrayTensorProduct(A, KroneckerProduct(B, x.T*x), C), [4, 5])

    # Always prefer matrix multiplication to Kronecker product, if possible:
    expr = ArrayTensorProduct(a, b, x.T*x)
    assert _remove_trivial_dims(expr) == (a*x.T*x*b.T, [1, 3, 4, 5])

