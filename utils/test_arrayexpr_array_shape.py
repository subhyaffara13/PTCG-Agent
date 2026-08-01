
def test_arrayexpr_array_shape():
    expr = _array_tensor_product(M, N, P, Q)
    assert expr.shape == (k, k, k, k, k, k, k, k)
    Z = MatrixSymbol("Z", m, n)
    expr = _array_tensor_product(M, Z)
    assert expr.shape == (k, k, m, n)
    expr2 = _array_contraction(expr, (0, 1))
    assert expr2.shape == (m, n)
    expr2 = _array_diagonal(expr, (0, 1))
    assert expr2.shape == (m, n, k)
    exprp = _permute_dims(expr, [2, 1, 3, 0])
    assert exprp.shape == (m, k, n, k)
    expr3 = _array_tensor_product(N, Z)
    expr2 = _array_add(expr, expr3)
    assert expr2.shape == (k, k, m, n)

    # Contraction along axes with discordant dimensions:
    raises(ValueError, lambda: _array_contraction(expr, (1, 2)))
    # Also diagonal needs the same dimensions:
    raises(ValueError, lambda: _array_diagonal(expr, (1, 2)))
    # Diagonal requires at least to axes to compute the diagonal:
    raises(ValueError, lambda: _array_diagonal(expr, (1,)))

