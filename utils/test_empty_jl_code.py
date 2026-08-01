
def test_empty_jl_code():
    code_gen = JuliaCodeGen()
    output = StringIO()
    code_gen.dump_jl([], output, "file", header=False, empty=False)
    source = output.getvalue()
    assert source == ""

