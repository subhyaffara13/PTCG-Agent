
def test_fcode_matrixsymbol_slice():
    A = MatrixSymbol('A', 2, 3)
    B = MatrixSymbol('B', 1, 3)
    C = MatrixSymbol('C', 1, 3)
    D = MatrixSymbol('D', 2, 1)
    name_expr = ("test", [Equality(B, A[0, :]),
                          Equality(C, A[1, :]),
                          Equality(D, A[:, 2])])
    result = codegen(name_expr, "f95", "test", header=False, empty=False)
    source = result[0][1]
    expected = (
        "subroutine test(A, B, C, D)\n"
        "implicit none\n"
        "REAL*8, intent(in), dimension(1:2, 1:3) :: A\n"
        "REAL*8, intent(out), dimension(1:1, 1:3) :: B\n"
        "REAL*8, intent(out), dimension(1:1, 1:3) :: C\n"
        "REAL*8, intent(out), dimension(1:2, 1:1) :: D\n"
        "B(1, 1) = A(1, 1)\n"
        "B(1, 2) = A(1, 2)\n"
        "B(1, 3) = A(1, 3)\n"
        "C(1, 1) = A(2, 1)\n"
        "C(1, 2) = A(2, 2)\n"
        "C(1, 3) = A(2, 3)\n"
        "D(1, 1) = A(1, 3)\n"
        "D(2, 1) = A(2, 3)\n"
        "end subroutine\n"
    )
    assert source == expected

