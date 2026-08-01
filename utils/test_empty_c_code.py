
def test_empty_c_code():
    code_gen = C89CodeGen()
    source = get_string(code_gen.dump_c, [])
    assert source == "#include \"file.h\"\n#include <math.h>\n"

