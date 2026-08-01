
def test_glsl_code_boolean():
    assert glsl_code(x & y) == "x && y"
    assert glsl_code(x | y) == "x || y"
    assert glsl_code(~x) == "!x"
    assert glsl_code(x & y & z) == "x && y && z"
    assert glsl_code(x | y | z) == "x || y || z"
    assert glsl_code((x & y) | z) == "z || x && y"
    assert glsl_code((x | y) & z) == "z && (x || y)"

