
def test_jl_numbersymbol():
    name_expr = ("test", pi**Catalan)
    result, = codegen(name_expr, "Julia", header=False, empty=False)
    source = result[1]
    expected = (
        "function test()\n"
        "    out1 = pi ^ catalan\n"
        "    return out1\n"
        "end\n"
    )
    assert source == expected

