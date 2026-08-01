
def test_glsl_code_exceptions():
    assert glsl_code(ceiling(x)) == "ceil(x)"
    assert glsl_code(Abs(x)) == "abs(x)"

