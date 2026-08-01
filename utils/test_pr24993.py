
def test_pr24993():
    from sympy.matrices.expressions.kronecker import matrix_kronecker_product
    from sympy.physics.quantum.matrixutils    import matrix_tensor_product
    X = Matrix([[0, 1], [1, 0]])
    Xi = ImmutableMatrix(X)
    assert TensorProduct(Xi, Xi) == TensorProduct(X, X)
    assert TensorProduct(Xi, Xi) == matrix_tensor_product(X, X)
    assert TensorProduct(Xi, Xi) == matrix_kronecker_product(X, X)

