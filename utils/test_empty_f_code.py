
def test_empty_f_code():
    code_gen = FCodeGen()
    source = get_string(code_gen.dump_f95, [])
    assert source == ""

