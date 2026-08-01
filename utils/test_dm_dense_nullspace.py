
def test_dm_dense_nullspace(name, A, A_null):
    A = A.to_field().to_dense()
    A_null_found = A.nullspace(divide_last=True)
    _check_divided(A_null_found, A_null)

