
def test_Matrix_nullspace(name, A, A_null):
    A = A.to_Matrix()

    A_null_cols = A.nullspace()

    # We have to patch up the case where the nullspace is empty
    if A_null_cols:
        A_null_found = Matrix.hstack(*A_null_cols)
    else:
        A_null_found = Matrix.zeros(A.cols, 0)

    A_null_found = A_null_found.to_DM().to_field().to_dense()

    # The Matrix result is the transpose of DomainMatrix result.
    A_null_found = A_null_found.transpose()

    _check_divided(A_null_found, A_null)

