
def test_glsl_code_constants_mathh():
    assert glsl_code(exp(1)) == "float E = 2.71828183;\nE"
    assert glsl_code(pi) == "float pi = 3.14159265;\npi"

