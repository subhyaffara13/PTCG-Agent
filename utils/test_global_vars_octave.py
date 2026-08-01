
def test_global_vars_octave():
    x, y, z, t = symbols("x y z t")
    result = codegen(('f', x*y), "Julia", header=False, empty=False,
                     global_vars=(y,))
    source = result[0][1]
    expected = (
        "function f(x)\n"
        "    out1 = x .* y\n"
        "    return out1\n"
        "end\n"
        )
    assert source == expected

    result = codegen(('f', x*y+z), "Julia", header=False, empty=False,
                     argument_sequence=(x, y), global_vars=(z, t))
    source = result[0][1]
    expected = (
        "function f(x, y)\n"
        "    out1 = x .* y + z\n"
        "    return out1\n"
        "end\n"
    )
    assert source == expected


def test_global_vars_octave():
    x, y, z, t = symbols("x y z t")
    result = codegen(('f', x*y), "Octave", header=False, empty=False,
                     global_vars=(y,))
    source = result[0][1]
    expected = (
        "function out1 = f(x)\n"
        "  global y\n"
        "  out1 = x.*y;\n"
        "end\n"
        )
    assert source == expected

    result = codegen(('f', x*y+z), "Octave", header=False, empty=False,
                     argument_sequence=(x, y), global_vars=(z, t))
    source = result[0][1]
    expected = (
        "function out1 = f(x, y)\n"
        "  global t z\n"
        "  out1 = x.*y + z;\n"
        "end\n"
    )
    assert source == expected

