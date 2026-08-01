
def test_jl_InOutArgument_order():
    # can specify the order as (x, y)
    expr = Equality(x, x**2 + y)
    name_expr = ("test", expr)
    result, = codegen(name_expr, "Julia", header=False,
                      empty=False, argument_sequence=(x,y))
    source = result[1]
    expected = (
        "function test(x, y)\n"
        "    x = x .^ 2 + y\n"
        "    return x\n"
        "end\n"
    )
    assert source == expected
    # make sure it gives (x, y) not (y, x)
    expr = Equality(x, x**2 + y)
    name_expr = ("test", expr)
    result, = codegen(name_expr, "Julia", header=False, empty=False)
    source = result[1]
    expected = (
        "function test(x, y)\n"
        "    x = x .^ 2 + y\n"
        "    return x\n"
        "end\n"
    )
    assert source == expected

