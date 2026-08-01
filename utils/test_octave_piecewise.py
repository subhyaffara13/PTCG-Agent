
def test_octave_piecewise():
    expr = Piecewise((x, x < 1), (x**2, True))
    assert mcode(expr) == "((x < 1).*(x) + (~(x < 1)).*(x.^2))"
    assert mcode(expr, assign_to="r") == (
        "r = ((x < 1).*(x) + (~(x < 1)).*(x.^2));")
    assert mcode(expr, assign_to="r", inline=False) == (
        "if (x < 1)\n"
        "  r = x;\n"
        "else\n"
        "  r = x.^2;\n"
        "end")
    expr = Piecewise((x**2, x < 1), (x**3, x < 2), (x**4, x < 3), (x**5, True))
    expected = ("((x < 1).*(x.^2) + (~(x < 1)).*( ...\n"
                "(x < 2).*(x.^3) + (~(x < 2)).*( ...\n"
                "(x < 3).*(x.^4) + (~(x < 3)).*(x.^5))))")
    assert mcode(expr) == expected
    assert mcode(expr, assign_to="r") == "r = " + expected + ";"
    assert mcode(expr, assign_to="r", inline=False) == (
        "if (x < 1)\n"
        "  r = x.^2;\n"
        "elseif (x < 2)\n"
        "  r = x.^3;\n"
        "elseif (x < 3)\n"
        "  r = x.^4;\n"
        "else\n"
        "  r = x.^5;\n"
        "end")
    # Check that Piecewise without a True (default) condition error
    expr = Piecewise((x, x < 1), (x**2, x > 1), (sin(x), x > 0))
    raises(ValueError, lambda: mcode(expr))

