
def test_jl_InOutArgument():
    expr = Equality(x, x**2)
    name_expr = ("mysqr", expr)
    result, = codegen(name_expr, "Julia", header=False, empty=False)
    source = result[1]
    expected = (
        "function mysqr(x)\n"
        "    x = x .^ 2\n"
        "    return x\n"
        "end\n"
    )
    assert source == expected

