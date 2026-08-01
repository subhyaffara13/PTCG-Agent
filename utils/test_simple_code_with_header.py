
def test_simple_code_with_header():
    name_expr = ("test", (x + y)*z)
    result, = codegen(name_expr, "Rust", header=True, empty=False)
    assert result[0] == "test.rs"
    source = result[1]
    version_str = "Code generated with SymPy %s" % sympy.__version__
    version_line = version_str.center(76).rstrip()
    expected = (
        "/*\n"
        " *%(version_line)s\n"
        " *\n"
        " *              See http://www.sympy.org/ for more information.\n"
        " *\n"
        " *                       This file is part of 'project'\n"
        " */\n"
        "fn test(x: f64, y: f64, z: f64) -> f64 {\n"
        "    let out1 = z*(x + y);\n"
        "    out1\n"
        "}\n"
    ) % {'version_line': version_line}
    assert source == expected

