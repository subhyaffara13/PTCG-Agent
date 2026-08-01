
def test_results_named_ordered():
    A, B, C = symbols('A,B,C')
    expr1 = Equality(C, (x + y)*z)
    expr2 = Equality(A, (x - y)*z)
    expr3 = Equality(B, 2*x)
    name_expr = ("test", [expr1, expr2, expr3])
    result = codegen(name_expr, "Julia", header=False, empty=False,
                     argument_sequence=(x, z, y))
    assert result[0][0] == "test.jl"
    source = result[0][1]
    expected = (
        "function test(x, z, y)\n"
        "    C = z .* (x + y)\n"
        "    A = z .* (x - y)\n"
        "    B = 2 * x\n"
        "    return C, A, B\n"
        "end\n"
    )
    assert source == expected


def test_results_named_ordered():
    A, B, C = symbols('A,B,C')
    expr1 = Equality(C, (x + y)*z)
    expr2 = Equality(A, (x - y)*z)
    expr3 = Equality(B, 2*x)
    name_expr = ("test", [expr1, expr2, expr3])
    result = codegen(name_expr, "Octave", header=False, empty=False,
                     argument_sequence=(x, z, y))
    assert result[0][0] == "test.m"
    source = result[0][1]
    expected = (
        "function [C, A, B] = test(x, z, y)\n"
        "  C = z.*(x + y);\n"
        "  A = z.*(x - y);\n"
        "  B = 2*x;\n"
        "end\n"
    )
    assert source == expected


def test_results_named_ordered():
    A, B, C = symbols('A,B,C')
    expr1 = Equality(C, (x + y)*z)
    expr2 = Equality(A, (x - y)*z)
    expr3 = Equality(B, 2*x)
    name_expr = ("test", [expr1, expr2, expr3])
    result = codegen(name_expr, "Rust", header=False, empty=False,
                     argument_sequence=(x, z, y))
    assert result[0][0] == "test.rs"
    source = result[0][1]
    expected = (
        "fn test(x: f64, z: f64, y: f64) -> (f64, f64, f64) {\n"
        "    let C = z*(x + y);\n"
        "    let A = z*(x - y);\n"
        "    let B = 2*x;\n"
        "    (C, A, B)\n"
        "}\n"
    )
    assert source == expected

