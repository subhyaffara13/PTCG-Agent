
def test_dm_sparse_nullspace_fracfree(name, A, A_null):
    A = A.to_sparse()
    A_null_found = A.nullspace()
    _check_primitive(A_null_found, A_null)

