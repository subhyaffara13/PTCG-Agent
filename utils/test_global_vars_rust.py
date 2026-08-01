
def test_global_vars_rust():
    x, y, z, t = symbols("x y z t")
    result = codegen(('f', x*y), "Rust", header=False, empty=False,
                     global_vars=(y,))
    source = result[0][1]
    expected = (
        "fn f(x: f64) -> f64 {\n"
        "    let out1 = x*y;\n"
        "    out1\n"
        "}\n"
        )
    assert source == expected

    result = codegen(('f', x*y+z), "Rust", header=False, empty=False,
                     argument_sequence=(x, y), global_vars=(z, t))
    source = result[0][1]
    expected = (
        "fn f(x: f64, y: f64) -> f64 {\n"
        "    let out1 = x*y + z;\n"
        "    out1\n"
        "}\n"
    )
    assert source == expected

