
def test_multiple_results_rust():
    # Here the output order is the input order
    expr1 = (x + y)*z
    expr2 = (x - y)*z
    name_expr = ("test", [expr1, expr2])
    result, = codegen(name_expr, "Rust", header=False, empty=False)
    source = result[1]
    expected = (
        "fn test(x: f64, y: f64, z: f64) -> (f64, f64) {\n"
        "    let out1 = z*(x + y);\n"
        "    let out2 = z*(x - y);\n"
        "    (out1, out2)\n"
        "}\n"
    )
    assert source == expected

