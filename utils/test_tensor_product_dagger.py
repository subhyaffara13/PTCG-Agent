
def test_tensor_product_dagger():
    assert Dagger(TensorProduct(I*A, B)) == \
        -I*TensorProduct(Dagger(A), Dagger(B))
    assert Dagger(TensorProduct(mat1, mat2)) == \
        TensorProduct(Dagger(mat1), Dagger(mat2))

