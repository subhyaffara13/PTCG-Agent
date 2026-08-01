
def test_XXM_fflu(DM):
    A = DM([[1, 2], [3, 4]])
    P, L, D, U = A.fflu()
    A_field = A.convert_to(QQ)
    P_field = P.convert_to(QQ)
    L_field = L.convert_to(QQ)
    D_field = D.convert_to(QQ)
    U_field = U.convert_to(QQ)
    assert P.shape == A.shape
    assert L.shape == A.shape
    assert D.shape == A.shape
    assert U.shape == A.shape
    assert P == DM([[1, 0], [0, 1]])
    assert L == DM([[1, 0], [3, -2]])
    assert D == DM([[1, 0], [0, -2]])
    assert U == DM([[1, 2], [0, -2]])
    assert L_field.matmul(D_field.inv()).matmul(U_field) == P_field.matmul(A_field)

