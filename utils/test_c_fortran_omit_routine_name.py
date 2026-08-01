
def test_c_fortran_omit_routine_name():
    x, y = symbols("x,y")
    name_expr = [("foo", 2*x)]
    result = codegen(name_expr, "F95", header=False, empty=False)
    expresult = codegen(name_expr, "F95", "foo", header=False, empty=False)
    assert result[0][1] == expresult[0][1]

    name_expr = ("foo", x*y)
    result = codegen(name_expr, "F95", header=False, empty=False)
    expresult = codegen(name_expr, "F95", "foo", header=False, empty=False)
    assert result[0][1] == expresult[0][1]

    name_expr = ("foo", Matrix([[x, y], [x+y, x-y]]))
    result = codegen(name_expr, "C89", header=False, empty=False)
    expresult = codegen(name_expr, "C89", "foo", header=False, empty=False)
    assert result[0][1] == expresult[0][1]

