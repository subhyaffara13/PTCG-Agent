
def test_fcode_matrixsymbol_slice_autoname():
    # see issue #8093
    A = MatrixSymbol('A', 2, 3)
    name_expr = ("test", A[:, 1])
    result = codegen(name_expr, "f95", "test", header=False, empty=False)
    source = result[0][1]
    expected = (
        "subroutine test(A, out_%(hash)s)\n"
        "implicit none\n"
        "REAL*8, intent(in), dimension(1:2, 1:3) :: A\n"
        "REAL*8, intent(out), dimension(1:2, 1:1) :: out_%(hash)s\n"
        "out_%(hash)s(1, 1) = A(1, 2)\n"
        "out_%(hash)s(2, 1) = A(2, 2)\n"
        "end subroutine\n"
    )
    # look for the magic number
    a = source.splitlines()[3]
    b = a.split('_')
    out = b[1]
    expected = expected % {'hash': out}
    assert source == expected

