
def test_piecewise_inline():
    # FIXME: how to pass inline to the RustCodePrinter?
    pw = Piecewise((0, x < -1), (x**2, x <= 1), (-x+2, x > 1), (1, True))
    name_expr = ("pwtest", pw)
    result, = codegen(name_expr, "Rust", header=False, empty=False,
                      inline=True)
    source = result[1]
    expected = (
        "fn pwtest(x: f64) -> f64 {\n"
        "    let out1 = if (x < -1) { 0 } else if (x <= 1) { x.powi(2) }"
        " else if (x > 1) { -x + 2 } else { 1 };\n"
        "    out1\n"
        "}\n"
    )
    assert source == expected

