
def test_fcode_results_named_ordered():
    x, y, z = symbols('x,y,z')
    B, C = symbols('B,C')
    A = MatrixSymbol('A', 1, 3)
    expr1 = Equality(A, Matrix([[1, 2, x]]))
    expr2 = Equality(C, (x + y)*z)
    expr3 = Equality(B, 2*x)
    name_expr = ("test", [expr1, expr2, expr3])
    result = codegen(name_expr, "f95", "test", header=False, empty=False,
                     argument_sequence=(x, z, y, C, A, B))
    source = result[0][1]
    expected = (
        "subroutine test(x, z, y, C, A, B)\n"
        "implicit none\n"
        "REAL*8, intent(in) :: x\n"
        "REAL*8, intent(in) :: z\n"
        "REAL*8, intent(in) :: y\n"
        "REAL*8, intent(out) :: C\n"
        "REAL*8, intent(out) :: B\n"
        "REAL*8, intent(out), dimension(1:1, 1:3) :: A\n"
        "C = z*(x + y)\n"
        "A(1, 1) = 1\n"
        "A(1, 2) = 2\n"
        "A(1, 3) = x\n"
        "B = 2*x\n"
        "end subroutine\n"
    )
    assert source == expected

