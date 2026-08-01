
def test_numbersymbol_inline():
    # FIXME: how to pass inline to the RustCodePrinter?
    name_expr = ("test", [pi**Catalan, EulerGamma])
    result, = codegen(name_expr, "Rust", header=False,
                      empty=False, inline=True)
    source = result[1]
    expected = (
        "fn test() -> (f64, f64) {\n"
        "    const Catalan: f64 = %s;\n"
        "    const EulerGamma: f64 = %s;\n"
        "    let out1 = PI.powf(Catalan);\n"
        "    let out2 = EulerGamma);\n"
        "    (out1, out2)\n"
        "}\n"
    ) % (Catalan.evalf(17), EulerGamma.evalf(17))
    assert source == expected

