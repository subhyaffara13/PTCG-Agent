
def test_m_numbersymbol_no_inline():
    # FIXME: how to pass inline=False to the OctaveCodePrinter?
    name_expr = ("test", [pi**Catalan, EulerGamma])
    result, = codegen(name_expr, "Octave", header=False,
                      empty=False, inline=False)
    source = result[1]
    expected = (
        "function [out1, out2] = test()\n"
        "  Catalan = 0.915965594177219;  % constant\n"
        "  EulerGamma = 0.5772156649015329;  % constant\n"
        "  out1 = pi^Catalan;\n"
        "  out2 = EulerGamma;\n"
        "end\n"
    )
    assert source == expected

