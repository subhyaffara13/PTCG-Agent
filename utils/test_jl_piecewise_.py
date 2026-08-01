
def test_jl_piecewise_():
    pw = Piecewise((0, x < -1), (x**2, x <= 1), (-x+2, x > 1), (1, True), evaluate=False)
    name_expr = ("pwtest", pw)
    result, = codegen(name_expr, "Julia", header=False, empty=False)
    source = result[1]
    expected = (
        "function pwtest(x)\n"
        "    out1 = ((x < -1) ? (0) :\n"
        "    (x <= 1) ? (x .^ 2) :\n"
        "    (x > 1) ? (2 - x) : (1))\n"
        "    return out1\n"
        "end\n"
    )
    assert source == expected

