
def test_jl_numbersymbol_no_inline():
    # FIXME: how to pass inline=False to the JuliaCodePrinter?
    name_expr = ("test", [pi**Catalan, EulerGamma])
    result, = codegen(name_expr, "Julia", header=False,
                      empty=False, inline=False)
    source = result[1]
    expected = (
        "function test()\n"
        "    Catalan = 0.915965594177219\n"
        "    EulerGamma = 0.5772156649015329\n"
        "    out1 = pi ^ Catalan\n"
        "    out2 = EulerGamma\n"
        "    return out1, out2\n"
        "end\n"
    )
    assert source == expected

