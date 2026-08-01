
def test_simple_code_nameout():
    expr = Equality(z, (x + y))
    name_expr = ("test", expr)
    result, = codegen(name_expr, "Rust", header=False, empty=False)
    source = result[1]
    expected = (
        "fn test(x: f64, y: f64) -> f64 {\n"
        "    let z = x + y;\n"
        "    z\n"
        "}\n"
    )
    assert source == expected

