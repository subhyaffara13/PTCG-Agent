
def test_output_arg_mixed_unordered():
    # named outputs are alphabetical, unnamed output appear in the given order
    from sympy.functions.elementary.trigonometric import (cos, sin)
    a = symbols("a")
    name_expr = ("foo", [cos(2*x), Equality(y, sin(x)), cos(x), Equality(a, sin(2*x))])
    result, = codegen(name_expr, "Rust", header=False, empty=False)
    assert result[0] == "foo.rs"
    source = result[1]
    expected = (
        "fn foo(x: f64) -> (f64, f64, f64, f64) {\n"
        "    let out1 = (2*x).cos();\n"
        "    let y = x.sin();\n"
        "    let out3 = x.cos();\n"
        "    let a = (2*x).sin();\n"
        "    (out1, y, out3, a)\n"
        "}\n"
    )
    assert source == expected

