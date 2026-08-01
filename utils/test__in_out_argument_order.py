
def test_InOutArgument_order():
    # can specify the order as (x, y)
    expr = Equality(x, x**2 + y)
    name_expr = ("test", expr)
    result, = codegen(name_expr, "Rust", header=False,
                      empty=False, argument_sequence=(x,y))
    source = result[1]
    expected = (
        "fn test(x: f64, y: f64) -> f64 {\n"
        "    let x = x.powi(2) + y;\n"
        "    x\n"
        "}\n"
    )
    assert source == expected
    # make sure it gives (x, y) not (y, x)
    expr = Equality(x, x**2 + y)
    name_expr = ("test", expr)
    result, = codegen(name_expr, "Rust", header=False, empty=False)
    source = result[1]
    expected = (
        "fn test(x: f64, y: f64) -> f64 {\n"
        "    let x = x.powi(2) + y;\n"
        "    x\n"
        "}\n"
    )
    assert source == expected

