
def test_jl_code_argument_order():
    expr = x + y
    routine = make_routine("test", expr, argument_sequence=[z, x, y], language="julia")
    code_gen = JuliaCodeGen()
    output = StringIO()
    code_gen.dump_jl([routine], output, "test", header=False, empty=False)
    source = output.getvalue()
    expected = (
        "function test(z, x, y)\n"
        "    out1 = x + y\n"
        "    return out1\n"
        "end\n"
    )
    assert source == expected

