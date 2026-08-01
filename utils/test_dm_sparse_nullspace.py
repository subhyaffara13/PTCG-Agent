
def test_dm_sparse_nullspace(name, A, A_null):
    A = A.to_field().to_sparse()
    A_null_found = A.nullspace(divide_last=True)
    _check_divided(A_null_found, A_null)

