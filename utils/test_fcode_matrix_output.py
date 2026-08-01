
def test_fcode_matrix_output():
    x, y, z = symbols('x,y,z')
    e1 = x + y
    e2 = Matrix([[x, y], [z, 16]])
    name_expr = ("test", (e1, e2))
    result = codegen(name_expr, "f95", "test", header=False, empty=False)
    source = result[0][1]
    expected = (
        "REAL*8 function test(x, y, z, out_%(hash)s)\n"
        "implicit none\n"
        "REAL*8, intent(in) :: x\n"
        "REAL*8, intent(in) :: y\n"
        "REAL*8, intent(in) :: z\n"
        "REAL*8, intent(out), dimension(1:2, 1:2) :: out_%(hash)s\n"
        "out_%(hash)s(1, 1) = x\n"
        "out_%(hash)s(2, 1) = z\n"
        "out_%(hash)s(1, 2) = y\n"
        "out_%(hash)s(2, 2) = 16\n"
        "test = x + y\n"
        "end function\n"
    )
    # look for the magic number
    a = source.splitlines()[5]
    b = a.split('_')
    out = b[1]
    expected = expected % {'hash': out}
    assert source == expected

