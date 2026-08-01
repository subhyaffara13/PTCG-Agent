
def test_m_piecewise_():
    pw = Piecewise((0, x < -1), (x**2, x <= 1), (-x+2, x > 1), (1, True), evaluate=False)
    name_expr = ("pwtest", pw)
    result, = codegen(name_expr, "Octave", header=False, empty=False)
    source = result[1]
    expected = (
        "function out1 = pwtest(x)\n"
        "  out1 = ((x < -1).*(0) + (~(x < -1)).*( ...\n"
        "  (x <= 1).*(x.^2) + (~(x <= 1)).*( ...\n"
        "  (x > 1).*(2 - x) + (~(x > 1)).*(1))));\n"
        "end\n"
    )
    assert source == expected

