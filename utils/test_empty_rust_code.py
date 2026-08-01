
def test_empty_rust_code():
    code_gen = RustCodeGen()
    output = StringIO()
    code_gen.dump_rs([], output, "file", header=False, empty=False)
    source = output.getvalue()
    assert source == ""

