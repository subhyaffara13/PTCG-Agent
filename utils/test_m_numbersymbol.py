
def test_m_numbersymbol():
    name_expr = ("test", pi**Catalan)
    result, = codegen(name_expr, "Octave", header=False, empty=False)
    source = result[1]
    expected = (
        "function out1 = test()\n"
        "  out1 = pi^%s;\n"
        "end\n"
    ) % Catalan.evalf(17)
    assert source == expected

