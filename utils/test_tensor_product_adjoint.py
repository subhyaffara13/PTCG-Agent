
def test_tensor_product_adjoint():
    assert KroneckerProduct(I*A, B).adjoint() == \
        -I*KroneckerProduct(A.adjoint(), B.adjoint())
    assert KroneckerProduct(mat1, mat2).adjoint() == \
        kronecker_product(mat1.adjoint(), mat2.adjoint())

