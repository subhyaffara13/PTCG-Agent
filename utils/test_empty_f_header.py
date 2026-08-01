
def test_empty_f_header():
    code_gen = FCodeGen()
    source = get_string(code_gen.dump_h, [])
    assert source == ""

