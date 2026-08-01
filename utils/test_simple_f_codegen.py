
def test_simple_f_codegen():
    x, y, z = symbols('x,y,z')
    expr = (x + y)*z
    result = codegen(
        ("test", expr), "F95", "file", header=False, empty=False)
    expected = [
        ("file.f90",
        "REAL*8 function test(x, y, z)\n"
        "implicit none\n"
        "REAL*8, intent(in) :: x\n"
        "REAL*8, intent(in) :: y\n"
        "REAL*8, intent(in) :: z\n"
        "test = z*(x + y)\n"
        "end function\n"),
        ("file.h",
        "interface\n"
        "REAL*8 function test(x, y, z)\n"
        "implicit none\n"
        "REAL*8, intent(in) :: x\n"
        "REAL*8, intent(in) :: y\n"
        "REAL*8, intent(in) :: z\n"
        "end function\n"
        "end interface\n")
    ]
    assert result == expected

