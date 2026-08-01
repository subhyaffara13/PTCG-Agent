
def test_jl_simple_code_with_header():
    name_expr = ("test", (x + y)*z)
    result, = codegen(name_expr, "Julia", header=True, empty=False)
    assert result[0] == "test.jl"
    source = result[1]
    expected = (
        "#   Code generated with SymPy " + sympy.__version__ + "\n"
        "#\n"
        "#   See http://www.sympy.org/ for more information.\n"
        "#\n"
        "#   This file is part of 'project'\n"
        "function test(x, y, z)\n"
        "    out1 = z .* (x + y)\n"
        "    return out1\n"
        "end\n"
    )
    assert source == expected

