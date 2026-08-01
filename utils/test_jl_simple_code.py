
def test_jl_simple_code():
    name_expr = ("test", (x + y)*z)
    result, = codegen(name_expr, "Julia", header=False, empty=False)
    assert result[0] == "test.jl"
    source = result[1]
    expected = (
        "function test(x, y, z)\n"
        "    out1 = z .* (x + y)\n"
        "    return out1\n"
        "end\n"
    )
    assert source == expected

