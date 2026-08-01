
def test_empty_m_code():
    code_gen = OctaveCodeGen()
    output = StringIO()
    code_gen.dump_m([], output, "file", header=False, empty=False)
    source = output.getvalue()
    assert source == ""

