
def test_LU_decomp():
    A = A3.copy()
    b = b3
    A, p = LU_decomp(A)
    y = L_solve(A, b, p)
    x = U_solve(A, y)
    assert p == [2, 1, 2, 3]
    assert [round(i, 14) for i in x] == [3.78953107960742, 2.9989094874591098,
            -0.081788440567070006, 3.8713195201744801, 2.9171210468920399]
    A = A4.copy()
    b = b4
    A, p = LU_decomp(A)
    y = L_solve(A, b, p)
    x = U_solve(A, y)
    assert p == [0, 3, 4, 3]
    assert [round(i, 14) for i in x] == [2.6383625899619201, 2.6643834462368399,
            0.79208015947958998, -2.5088376454101899, -1.0567657691375001]
    A = randmatrix(3)
    bak = A.copy()
    LU_decomp(A, overwrite=1)
    assert A != bak

