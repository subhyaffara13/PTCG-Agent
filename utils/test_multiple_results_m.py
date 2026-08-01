
def test_multiple_results_m():
    # Here the output order is the input order
    expr1 = (x + y)*z
    expr2 = (x - y)*z
    name_expr = ("test", [expr1, expr2])
    result, = codegen(name_expr, "Julia", header=False, empty=False)
    source = result[1]
    expected = (
        "function test(x, y, z)\n"
        "    out1 = z .* (x + y)\n"
        "    out2 = z .* (x - y)\n"
        "    return out1, out2\n"
        "end\n"
    )
    assert source == expected


def test_multiple_results_m():
    # Here the output order is the input order
    expr1 = (x + y)*z
    expr2 = (x - y)*z
    name_expr = ("test", [expr1, expr2])
    result, = codegen(name_expr, "Octave", header=False, empty=False)
    source = result[1]
    expected = (
        "function [out1, out2] = test(x, y, z)\n"
        "  out1 = z.*(x + y);\n"
        "  out2 = z.*(x - y);\n"
        "end\n"
    )
    assert source == expected

