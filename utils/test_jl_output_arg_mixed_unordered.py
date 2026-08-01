
def test_jl_output_arg_mixed_unordered():
    # named outputs are alphabetical, unnamed output appear in the given order
    from sympy.functions.elementary.trigonometric import (cos, sin)
    a = symbols("a")
    name_expr = ("foo", [cos(2*x), Equality(y, sin(x)), cos(x), Equality(a, sin(2*x))])
    result, = codegen(name_expr, "Julia", header=False, empty=False)
    assert result[0] == "foo.jl"
    source = result[1]
    expected = (
        'function foo(x)\n'
        '    out1 = cos(2 * x)\n'
        '    y = sin(x)\n'
        '    out3 = cos(x)\n'
        '    a = sin(2 * x)\n'
        '    return out1, y, out3, a\n'
        'end\n'
    )
    assert source == expected

