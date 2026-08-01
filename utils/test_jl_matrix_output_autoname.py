
def test_jl_matrix_output_autoname():
    expr = Matrix([[x, x+y, 3]])
    name_expr = ("test", expr)
    result, = codegen(name_expr, "Julia", header=False, empty=False)
    source = result[1]
    expected = (
        "function test(x, y)\n"
        "    out1 = [x x + y 3]\n"
        "    return out1\n"
        "end\n"
    )
    assert source == expected

