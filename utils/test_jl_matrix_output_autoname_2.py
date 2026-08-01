
def test_jl_matrix_output_autoname_2():
    e1 = (x + y)
    e2 = Matrix([[2*x, 2*y, 2*z]])
    e3 = Matrix([[x], [y], [z]])
    e4 = Matrix([[x, y], [z, 16]])
    name_expr = ("test", (e1, e2, e3, e4))
    result, = codegen(name_expr, "Julia", header=False, empty=False)
    source = result[1]
    expected = (
        "function test(x, y, z)\n"
        "    out1 = x + y\n"
        "    out2 = [2 * x 2 * y 2 * z]\n"
        "    out3 = [x, y, z]\n"
        "    out4 = [x  y;\n"
        "    z 16]\n"
        "    return out1, out2, out3, out4\n"
        "end\n"
    )
    assert source == expected

