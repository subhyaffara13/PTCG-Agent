
def test_m_code_argument_order():
    expr = x + y
    routine = make_routine("test", expr, argument_sequence=[z, x, y], language="octave")
    code_gen = OctaveCodeGen()
    output = StringIO()
    code_gen.dump_m([routine], output, "test", header=False, empty=False)
    source = output.getvalue()
    expected = (
        "function out1 = test(z, x, y)\n"
        "  out1 = x + y;\n"
        "end\n"
    )
    assert source == expected

