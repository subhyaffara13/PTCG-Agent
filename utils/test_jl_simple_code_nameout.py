
def test_jl_simple_code_nameout():
    expr = Equality(z, (x + y))
    name_expr = ("test", expr)
    result, = codegen(name_expr, "Julia", header=False, empty=False)
    source = result[1]
    expected = (
        "function test(x, y)\n"
        "    z = x + y\n"
        "    return z\n"
        "end\n"
    )
    assert source == expected

