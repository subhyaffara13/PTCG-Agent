
def test_ccode_ITE():
    expr = ITE(x < 1, y, z)
    assert ccode(expr) == (
            "((x < 1) ? (\n"
            "   y\n"
            ")\n"
            ": (\n"
            "   z\n"
            "))")

