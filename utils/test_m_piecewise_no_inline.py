
def test_m_piecewise_no_inline():
    # FIXME: how to pass inline=False to the OctaveCodePrinter?
    pw = Piecewise((0, x < -1), (x**2, x <= 1), (-x+2, x > 1), (1, True))
    name_expr = ("pwtest", pw)
    result, = codegen(name_expr, "Octave", header=False, empty=False,
                      inline=False)
    source = result[1]
    expected = (
        "function out1 = pwtest(x)\n"
        "  if (x < -1)\n"
        "    out1 = 0;\n"
        "  elseif (x <= 1)\n"
        "    out1 = x.^2;\n"
        "  elseif (x > 1)\n"
        "    out1 = -x + 2;\n"
        "  else\n"
        "    out1 = 1;\n"
        "  end\n"
        "end\n"
    )
    assert source == expected

