
def test_empty_c_header():
    code_gen = C99CodeGen()
    source = get_string(code_gen.dump_h, [])
    assert source == "#ifndef PROJECT__FILE__H\n#define PROJECT__FILE__H\n#endif\n"

