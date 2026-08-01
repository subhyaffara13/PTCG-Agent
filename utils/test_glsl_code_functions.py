
def test_glsl_code_functions():
    assert glsl_code(sin(x) ** cos(x)) == "pow(sin(x), cos(x))"

