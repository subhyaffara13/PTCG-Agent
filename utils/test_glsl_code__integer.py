
def test_glsl_code_Integer():
    assert glsl_code(Integer(67)) == "67"
    assert glsl_code(Integer(-1)) == "-1"

