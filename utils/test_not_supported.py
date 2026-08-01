
def test_not_supported():
    f = Function('f')
    name_expr = ("test", [f(x).diff(x), S.ComplexInfinity])
    result, = codegen(name_expr, "Rust", header=False, empty=False)
    source = result[1]
    expected = (
        "fn test(x: f64) -> (f64, f64) {\n"
        "    // unsupported: Derivative(f(x), x)\n"
        "    // unsupported: zoo\n"
        "    let out1 = Derivative(f(x), x);\n"
        "    let out2 = zoo;\n"
        "    (out1, out2)\n"
        "}\n"
    )
    assert source == expected


def test_not_supported():
    f = Function('f')
    with _check_warns([_W.DEFAULTING_TO_FLOAT, _W.WILL_NOT_ASSERT]) as w:
        raises(KeyError, lambda: smtlib_code(f(x).diff(x), symbol_table={f: Callable[[float], float]}, log_warn=w))
    with _check_warns([_W.WILL_NOT_ASSERT]) as w:
        raises(KeyError, lambda: smtlib_code(S.ComplexInfinity, log_warn=w))

